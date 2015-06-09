from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from education.models import CheckIn, Student, Lecture

from django.conf import settings
from education.serializers import LectureSerializer, CheckInSerializer


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


@api_view(['GET'])
# @permission_classes((IsLecturer,))
def get_lectures(request):
    course_id = request.GET.get('course_id')
    lectures = Lecture.objects.filter(course_id=course_id)
    serializer = LectureSerializer(lectures, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes((IsLecturer,))
def get_check_ins(request):
    student_id = request.GET.get('student_id')
    check_ins = CheckIn.objects.filter(student_id=student_id)
    serializer = CheckInSerializer(check_ins, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
