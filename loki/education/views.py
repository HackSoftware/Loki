from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from education.models import CheckIn, Student

from django.conf import settings


@csrf_exempt
@require_POST
def set_check_in(request):
    mac = request.POST['mac']
    token = request.POST['token']

    if settings.CHECKIN_TOKEN != token:
        return HttpResponse(status=511)

    student = Student.objects.filter(mac__iexact=mac).first()
    if not student:
        student = None
    try:
        check_in = CheckIn(mac=mac, student=student)
        check_in.save()
    except IntegrityError:
        return HttpResponse(status=418)

    return HttpResponse(status=200)
