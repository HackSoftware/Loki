import os
import hmac
import time
import base64
import hashlib
import requests

from PIL import Image
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import CheckIn, Student, GraderRequest, Lecture, Solution


def crop_image(x1, y1, x2, y2, path):
    name = settings.MEDIA_ROOT + 'avatar/' + 'cropped_' + path[2:]
    try:
        image = Image.open(os.path.join(settings.MEDIA_ROOT, path[2:]))
    except IOError:
        return False
    img = image.crop((x1, y1, y2, x2))
    img.save(name)
    return settings.MEDIA_URL + 'avatar/' + 'cropped_' + path[2:]


def check_macs_for_student(student, mac):
    check_ins = CheckIn.objects.filter(mac__iexact=mac)
    for check_in in check_ins:
        if not check_in.student and check_in.mac.lower() == mac.lower():
            check_in.student = student
            check_in.save()


def mac_is_used_by_another_student(student, mac):
    student_db = Student.objects.filter(mac__iexact=mac).all()
    if not student_db:
        return False
    if len(student_db) > 2 or student_db.first() != student:
        return True
    return False


def get_and_update_req_nonce(req_and_resource):
    request = GraderRequest.objects.filter(request_info=req_and_resource).first()

    if request is not None:
        nonce = request.nonce
        nonce += 1
        request.nonce = nonce
        request.save()
        return str(nonce)
    else:
        nonce = 1
        GraderRequest.objects.create(nonce=nonce, request_info=req_and_resource)
        return str(nonce)


def generate_grader_headers(body, req_and_resource):
    nonce = get_and_update_req_nonce(req_and_resource)
    date = time.strftime("%c")
    msg = body + date + nonce
    digest = hmac.new(bytearray(settings.GRADER_API_SECRET.encode('utf-8')),
                      msg=msg.encode('utf-8'),
                      digestmod=hashlib.sha256).hexdigest()

    request_headers = {'Authentication': digest,
                       'Date': date,
                       'X-API-Key': settings.GRADER_API_KEY,
                       'X-Nonce-Number': nonce}

    return request_headers


def get_solution_code(url):
    # Create raw github url
    raw_solution_url = "/".join(
        [x for x in url.split("/") if x != "blob"]).replace(
        "github", "raw.githubusercontent")

    r = requests.get(raw_solution_url)
    return r.text


def update_req_and_resource_nonce(req_and_resource, nonce):
    grader_request = get_object_or_404(GraderRequest, request_info=req_and_resource)
    grader_request.nonce = nonce
    grader_request.save()


def read_binary_file(path):
    """Returns the file in base64 encoding"""

    with open(path, 'rb') as f:
        encoded = base64.b64encode(f.read())

    return encoded.decode('ascii')


def get_dates_for_weeks(course):
    lectures = course.lecture_set.filter(week__isnull=False).values('week', 'date')
    week_dates = {}

    for lecture in lectures:
        week = lecture['week']
        if week not in week_dates:
            week_dates[week] = [lecture['date']]
        else:
            week_dates[week].append(lecture['date'])

    return week_dates


def task_solutions(solutions):
    task_solutions = {}
    for solution in solutions:
        task_name = solution.task.name
        if task_name not in task_solutions:
            task_solutions[task_name] = [solution]
        elif task_name in task_solutions:
            task_solutions[task_name].append(solution)
        else:
            task_solutions.update({task_name: solution})

    return task_solutions


def latest_solution_statuses(user, tasks):
    latest_solutions = {}
    for task in tasks:
        task_name = task.name
        solution = Solution.objects.get_latest_solution(user, task)
        if solution:
            latest_solutions[task_name] = solution.get_status_display()
    return latest_solutions


def percentage_presence(student_dates, course):
    lecture_dates = Lecture.objects.filter(course=course,
                                           date__lte=timezone.now().date()).values_list(
                                           'date', flat=True)
    student_dates = [date for date in student_dates if date in lecture_dates]
    # import ipdb; ipdb.set_trace()

    return "{0}%".format(int((len(student_dates) / len(lecture_dates)) * 100))
