import os
from PIL import Image
from django.conf import settings
from education.models import CheckIn, Student


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
