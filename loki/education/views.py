from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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


class OnBoardStudent(APIView):
    permission_classes = (IsAuthenticated,)

    def make_student(self, baseuser):
        student = Student(baseuser_ptr_id=baseuser.id)
        student.save()
        student.__dict__.update(baseuser.__dict__)
        return student.save()

    def post(self, request, format=None):
        if not request.user.get_student():
            self.make_student(request.user)
            return Response(status=status.HTTP_200_OK)
