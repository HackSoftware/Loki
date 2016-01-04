from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from base_app.models import City, Company

from .premissions import IsStudent, IsTeacher, IsTeacherForCA

from .models import (CheckIn, Student, Lecture, Course, CourseAssignment, WorkingAt,
                     Task, Solution, Certificate, Test)

from .serializers import (UpdateStudentSerializer, StudentNameSerializer,
                          LectureSerializer, CheckInSerializer, CourseSerializer, FullCASerializer,
                          SolutionSerializer, CourseAssignmentSerializer, WorkingAtSerializer,
                          CitySerializer, CompanySerializer, TaskSerializer, StudentNoteSerializer,
                          SolutionStatusSerializer)

from education.helper import (check_macs_for_student, mac_is_used_by_another_student,
                              generate_grader_headers)

import requests
import json


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
@permission_classes((IsAuthenticated,))
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


# TODO: Refactor mac checks
@api_view(['PATCH'])
@permission_classes((IsStudent,))
def student_update(request):
    student = request.user.get_student()
    if 'mac' in request.data:
        if mac_is_used_by_another_student(student, request.data['mac']):
            error = {"error": "Този мак в вече зает"}
            return Response(error, status=400)
        check_macs_for_student(student, request.data['mac'])
    serializer = UpdateStudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes((IsStudent,))
def get_students_for_course(request):
    course_id = request.GET.get('course_id')
    students = get_object_or_404(Course, id=course_id).student_set
    serializer = StudentNameSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CourseAssignmentAPI(generics.ListAPIView):
    model = CourseAssignment
    serializer_class = FullCASerializer
    permission_classes = (IsTeacher,)
    filter_fields = ('course__id',)

    def get_queryset(self):
        teached_courses = self.request.user.teacher.teached_courses.all()
        return CourseAssignment.objects.filter(course__in=teached_courses)


class StudentNoteAPI(generics.CreateAPIView):
    permission_classes = (IsTeacher, IsTeacherForCA)
    serializer_class = StudentNoteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.get_teacher())


@api_view(['PATCH'])
@permission_classes((IsTeacher,))
def drop_student(request):
    cas = get_object_or_404(CourseAssignment, id=request.data['ca_id'])
    serializer = CourseAssignmentSerializer(cas, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PATCH'])
@permission_classes((IsAuthenticated,))
def working_at(request):
    if request.method == 'POST':
        serializer = WorkingAtSerializer(data=request.data)
        if serializer.is_valid():
            company = Company.objects.filter(name__iexact=serializer.data['company_name']).first()
            if company:
                obj = serializer.save(student=request.user.student, company=company)
            else:
                obj = serializer.save(student=request.user.student)
            return Response(WorkingAtSerializer(obj).data, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        working_at_entry = get_object_or_404(WorkingAt, id=request.data['working_at_id'])
        serializer = WorkingAtSerializer(working_at_entry, data=request.data, partial=True)
        if serializer.is_valid():
            company = Company.objects.filter(name__iexact=serializer.data['company_name']).first()
            if company:
                obj = serializer.save(student=request.user.student, company=company)
            else:
                obj = serializer.save(student=request.user.student)
            return Response(WorkingAtSerializer(obj).data, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cities(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_companies(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class TasksAPI(generics.ListAPIView):
    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsStudent,)
    filter_fields = ('course__id',)


class SolutionStatusAPI(
        mixins.RetrieveModelMixin,
        generics.GenericAPIView):
    model = Solution
    serializer_class = SolutionStatusSerializer
    permission_classes = (IsStudent,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_queryset(self):
        student = self.request.user.get_student()
        return student.solution_set


class SolutionsAPI(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        generics.GenericAPIView):
    model = Solution
    serializer_class = SolutionSerializer
    permission_classes = (IsStudent,)
    filter_fields = ('task__course__id',)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_create(self, serializer):
        solution = serializer.save(student=self.request.user.get_student())
        self.send_to_grader(solution)

    def perform_update(self, serializer):
        solution = serializer.save()
        self.send_to_grader(solution)

    def get_queryset(self):
        student = self.request.user.get_student()
        return student.solution_set

    def send_to_grader(self, solution):

        data = {
            "test_type": Test.TYPE_CHOICE[solution.task.test.test_type][1],
            "language": solution.task.test.language.name,
            "code": solution.code,
            "test": solution.task.test.code,
        }

        address = settings.GRADER_ADDRESS
        path = "/grade"
        url = address + path

        req_and_resource = "POST {}".format(path)

        headers = generate_grader_headers(json.dumps(data), req_and_resource)
        r = requests.post(url, json=data, headers=headers)

        if r.status_code == 202:
            solution.build_id = r.json()['run_id']
            solution.save()
        else:
            raise Exception(r.text)


def certificate(request, pk):
    certificate = get_object_or_404(Certificate, id=pk)
    ca = certificate.assignment
    student = ca.user
    course = ca.course

    tasks = Task.objects.filter(course=ca.course)
    solutions = Solution.objects.filter(task__in=tasks, student=ca.user)
    percent_awesome = round((solutions.count() / tasks.count()) * 100, 2)

    tasks_solutions = {solution.task: solution for solution in solutions}

    for task in tasks:
        if task in tasks_solutions:
            task.solution = tasks_solutions[task]

    return render(request, "certificate.html", locals())
