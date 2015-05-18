from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from education.models import CheckIn, Student
from loki import local_settings


@require_http_methods(['POST'])
def set_check_in(request):
    mac = request.POST['mac']
    token = request.POST['token']

    if local_settings.CHECKIN_TOKEN != token:
        return HttpResponse(status=511)

    student = Student.objects.filter(mac__iexact=mac)
    if not student:
        student = None
    try:
        check_in = CheckIn(mac=mac, student=student)
        check_in.save()
    except IntegrityError:
        return HttpResponse(status=418)

    return HttpResponse(status=200)
