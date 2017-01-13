from __future__ import absolute_import

import json
import requests
import time
import subprocess

from django.conf import settings
from loki.celery import app

from .models import Test, Solution, RetestSolution
from .helper import (generate_grader_headers, get_solution_code,
                     update_req_and_resource_nonce, read_binary_file)


@app.task
def submit_solution(solution_id):
    solution = Solution.objects.get(id=solution_id)

    if solution.code is None and solution.file is None:
        solution.code = get_solution_code(solution.url)
        solution.save()

    if solution.task.test.is_source():
        data = get_plain_problem_data(solution)
    else:
        data = get_binary_problem_data(solution)

    address = settings.GRADER_ADDRESS
    path = settings.GRADER_GRADE_PATH
    url = address + path
    req_and_resource = "POST {}".format(path)
    headers = generate_grader_headers(json.dumps(data), req_and_resource)

    r = requests.post(url, json=data, headers=headers)
    if r.status_code == 202:
        solution.status = Solution.PENDING
        solution.build_id = r.json()['run_id']
        solution.check_status_location = r.headers['Location']
        solution.save()

        poll_solution.delay(solution_id)
    else:
        raise Exception(r.text)


def get_binary_problem_data(solution):

    data = {"test_type": Test.TYPE_CHOICE[solution.task.test.test_type][1],
            "language": solution.task.test.language.name,
            "file_type": "binary",
            "code": read_binary_file("{}{}".format(settings.MEDIA_ROOT,
                                                   solution.file)),
            "test": read_binary_file("{}{}".format(settings.MEDIA_ROOT,
                                                   solution.task.test.binaryfiletest.file)),
            "extra_options": solution.task.test.options}

    return data


def get_plain_problem_data(solution):
    data = {"test_type": Test.TYPE_CHOICE[solution.task.test.test_type][1],
            "language": solution.task.test.language.name,
            "file_type": 'plain',
            "code": solution.code,
            "test": solution.task.test.sourcecodetest.code,
            "extra_options": solution.task.test.options}

    return data


@app.task
def poll_solution(solution_id):
    solution = Solution.objects.get(id=solution_id)

    path = settings.GRADER_CHECK_PATH.format(buildID=solution.build_id)
    url = solution.check_status_location
    req_and_resource = "GET {}".format(path)

    while True:
        headers = generate_grader_headers(path, req_and_resource)
        r = requests.get(url, headers=headers)
        if r.status_code == 403 and r.text == "Nonce check failed":
            get_nonce_url = settings.GRADER_ADDRESS + settings.GRADER_GET_NONCE_PATH

            headers = {
                'Request-Info': req_and_resource,
                'X-USER-Key': settings.GRADER_API_KEY
            }

            responce = requests.get(get_nonce_url, headers=headers)
            nonce = responce.json()["nonce"]
            update_req_and_resource_nonce(req_and_resource, nonce)

        elif r.status_code == 200:
            data = r.json()

            if data['result_status'] == 'ok':
                solution.status = Solution.OK
            elif data['result_status'] == 'not_ok':
                solution.status = Solution.NOT_OK

            solution.test_output = data['output']['test_output']
            solution.save()
            break

        time.sleep(settings.POLLING_SLEEP_TIME)


@app.task
def check_for_retests():
    status_choices = {
        "pending": 0,
        "done": 1
    }

    pending_retests = RetestSolution.objects.filter(status=status_choices["pending"])
    for pending_retest in pending_retests:
        test = Test.objects.get(id=pending_retest.test_id)
        solutions_to_be_tested = Solution.objects.filter(task__test=test)
        for solution in solutions_to_be_tested:
            retest_solution.delay(solution.id)
        pending_retest.status = status_choices["done"]
        pending_retest.save()


@app.task
def retest_solution(solution_id):
    solution = Solution.objects.get(id=solution_id)
    solution.status = Solution.SUBMITED
    submit_solution.delay(solution.id)

@app.task
def execute_calculate_presense_command():
    subprocess.call('python manage.py calculate_presence', shell=True, close_fds=True)
