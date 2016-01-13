from PIL import Image
from django.conf import settings
from education.models import CheckIn, Student, GraderRequest
import os
import time
import hmac
import hashlib
import requests


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
        request.nonce += 1
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


def get_solution_code(solution):
    if solution.code is not None:
        return solution.code
    # Create raw github url
    url = "/".join(
        [x for x in solution.url.split("/") if x != "blob"]).replace(
        "github", "raw.githubusercontent")
    # Extract the code
    r = requests.get(url)
    solution.code = r.text
    solution.save()
    return r.text
