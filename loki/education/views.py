from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

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


class RegisterStudent(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        if not request.user.is_authenticated():
            return redirect('base_app:register')
        elif request.user.is_authenticated() and request.user.get_student():
            pass
            # връща, че вече си регистриран
        elif request.user.is_authenticated() and request.user.get_student():
            pass
            # формичка за допълване

    def post(self, request, format=None):
        if request.user.is_authenticated() and not request.user.get_student():
            Student.objects.create(
                baseuser_ptr_id=self.id
                # more info
            )
        else:
            pass
            # нямаш право да постваш
