from __future__ import absolute_import

from loki.celery import app
from django.conf import settings

from .models import Test, Solution, RetestSolution
from .helper import generate_grader_headers, get_solution_code

import json
import requests
import time


@app.task
def submit_solution(solution_id):
    solution = Solution.objects.get(id=solution_id)

    if solution.code is None:
        solution.code = get_solution_code(solution.url)
        solution.save()

    data = {
        "test_type": Test.TYPE_CHOICE[solution.task.test.test_type][1],
        "language": solution.task.test.language.name,
        "code": solution.code,
        "test": solution.task.test.code,
    }

    address = settings.GRADER_ADDRESS
    path = settings.GRADER_GRADE_PATH
    url = address + path
    req_and_resource = "POST {}".format(path)
    headers = generate_grader_headers(json.dumps(data), req_and_resource)

    r = requests.post(url, json=data, headers=headers)
    if r.status_code == 202:
        solution.build_id = r.json()['run_id']
        solution.check_status_location = r.headers['Location']
        solution.save()

        poll_solution.delay(solution_id)
    else:
        raise Exception(r.text)


@app.task
def poll_solution(solution_id):
    solution = Solution.objects.get(id=solution_id)

    path = settings.GRADER_CHECK_PATH.format(solution.build_id)
    url = solution.check_status_location
    req_and_resource = "GET {}".format(path)

    while True:
        headers = generate_grader_headers(path, req_and_resource)
        r = requests.get(url, headers=headers)

        if r.status_code == 204:
            solution.status = Solution.PENDING
        elif r.status_code == 200:
            data = r.json()

            if data['result_status'] == 'ok':
                solution.status = Solution.OK
            elif data['result_status'] == 'not_ok':
                solution.status = Solution.NOT_OK

            solution.test_output = data['output']
            solution.return_code = data['returncode']
            solution.save()
            break

        time.sleep(1)


@app.task
def retest_solutions():
    status_choices = {
        "pending": 0,
        "done": 1
    }
    pending_retests = RetestSolution.objects.filter(status=status_choices["pending"])
    for pending_retest in pending_retests:
        test = Test.objects.get(id=pending_retest.test_id)
        solutions_to_be_tested = Solution.objects.filter(task__test=test)
        print(solutions_to_be_tested)
        for solution in solutions_to_be_tested:
            poll_solution.delay(solution.id)
        pending_retest.status = status_choices["done"]
        pending_retest.save()
