from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CheckIn, Student, Lecture, Course, CourseAssignment, StudentNote
from .serializers import (UpdateStudentSerializer, StudentNameSerializer,
                          LectureSerializer, CheckInSerializer, CourseSerializer, FullCASerializer)
from .premissions import IsStudent, IsTeacher


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
@permission_classes((IsTeacher,))
def get_lectures(request):
    course_id = request.GET.get('course_id')
    lectures = Lecture.objects.filter(course_id=course_id)
    serializer = LectureSerializer(lectures, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_check_ins(request):
    student_id = request.GET.get('student_id')
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)
    start_time = course.start_time
    end_time = course.end_time
    check_ins = CheckIn.objects.filter(student_id=student_id,
                                       date__gte=start_time,
                                       date__lte=end_time)
    serializer = CheckInSerializer(check_ins, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_courses(request):
    teacher = request.user.get_teacher()
    courses = teacher.teached_courses.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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


@api_view(['PATCH'])
@permission_classes((IsStudent,))
def student_update(request):
    student = request.user.get_student()
    serializer = UpdateStudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes((IsTeacher,))
def get_students_for_course(request):
    course_id = request.GET.get('course_id')
    students = get_object_or_404(Course, id=course_id).student_set
    serializer = StudentNameSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsTeacher,))
# TODO: Add IsTeacherForThatCourse
def get_cas_for_course(request):
    course_id = request.GET.get('course_id')
    course = get_object_or_404(Course, id=course_id)
    cas = CourseAssignment.objects.filter(course=course)
    serializer = FullCASerializer(cas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsTeacher,))
def create_student_note(request):
    teacher = request.user.get_teacher()
    ca = get_object_or_404(CourseAssignment, id=request.data['ca_id'])
    if ca.course not in teacher.teached_courses.all():
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    text = request.data['text']
    StudentNote.objects.create(
        text=text,
        assignment=ca,
        author=teacher
    )
    message = {"message": "Успешно написахте коментар за студента"}
    return Response(message, status=status.HTTP_201_CREATED)
