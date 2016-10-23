import uuid
import base64

from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

from rest_framework import serializers, generics, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from loki.base_app.models import City, Company

from ..premissions import IsStudent, IsTeacher, IsTeacherForCA
from ..models import (CheckIn, Student, Lecture, Course, CourseAssignment,
                      WorkingAt, Task, Solution, Certificate)
from ..serializers import (UpdateStudentSerializer, StudentNameSerializer,
                           LectureSerializer, CheckInSerializer, CourseSerializer, FullCASerializer,
                           SolutionSerializer, CourseAssignmentSerializer, WorkingAtSerializer,
                           CitySerializer, CompanySerializer, TaskSerializer, StudentNoteSerializer,
                           SolutionStatusSerializer)
from ..helper import (check_macs_for_student, mac_is_used_by_another_student)
from ..tasks import submit_solution


@csrf_exempt
@require_POST
def set_check_in(request):
    mac = request.POST['mac']
    token = request.POST['token']

    if settings.CHECKIN_TOKEN != token:
        return HttpResponse(status=511)

    student = Student.objects.filter(mac=mac).first()
    if not student:
        student = None
    try:
        check_in = CheckIn(mac=mac, student=student)
        check_in.save()
    except IntegrityError:
        return HttpResponse(status=418)

    return HttpResponse(status=200)


class GetLectures(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = LectureSerializer

    def get_queryset(self, request):
        course_id = self.request.GET.get('course_id')
        return Lecture.objects.filter(course_id=course_id)


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
            company = Company.objects.filter(name__iexact=serializer.initial_data['company_name']).first()
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
            company = Company.objects.filter(name__iexact=working_at_entry.company_name).first()
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
    permission_classes = (IsAuthenticated,)
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


class StudentSolutionsList(generics.ListAPIView):
    serializer_class = SolutionSerializer
    permission_classes = (IsTeacher,)

    def get_queryset(self):
        queryset = Solution.objects.filter(task__course__teacher=self.request.user)
        student_id = self.request.query_params.get('student_id', None)
        course_id = self.request.query_params.get('course_id', None)
        if student_id is not None:
            queryset = queryset.filter(student__id=student_id)
        if course_id is not None:
            queryset = queryset.filter(task__course__id=course_id)
        return queryset


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

    ''' Pre-create validations
    '''
    def post(self, request, *args, **kwargs):
        data = request.data
        url = data.get('url', None)
        code = data.get('code', None)
        file = data.get('file', None)

        '''
            Solutions without code or url are not accepted
        '''
        if not url and not code and not file:
            raise serializers.ValidationError('Either code, file or url should be given.')

        '''
            If task is not gradable, we should have url
        '''
        task = get_object_or_404(Task, pk=data['task'])

        if not task.gradable and not url and not file:
            raise serializers.ValidationError('Non-gradable tasks require GitHub url or a file')

        if file is not None:
            file = base64.b64decode(request.data['file'])
            request.data['file'] = ContentFile(content=file, name=str(uuid.uuid4()))

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        solution = serializer.save(student=self.request.user.get_student())

        if solution.task.gradable:
            solution.status = Solution.SUBMITED
            solution.save()

            solution_id = solution.id
            submit_solution.delay(solution_id)

    def get_queryset(self):
        student = self.request.user.get_student()
        return student.solution_set


def certificate_old(request, pk):
    return render(request, "certificate_old.html", locals())


def certificate(request, token):
    certificate = get_object_or_404(Certificate, token=token)
    ca = certificate.assignment
    student = ca.user
    course = ca.course
    teachers = course.teacher_set.all()

    tasks = Task.objects.filter(course=ca.course)
    solutions = Solution.objects.filter(task__in=tasks, student=ca.user)
    task_to_solution = {solution.task: solution for solution in solutions}

    projects = tasks.filter(gradable=False)
    problems = tasks.filter(gradable=True)

    solved_projects_count = 0
    solved_problems_count = 0

    for project in projects:
        if project.solution_set.count() >= 0:
            solved_projects_count += 1

    for problem in problems:
        current_solutions = problem.solution_set.all()

        if current_solutions.count() > 0 and current_solutions.last().status == 'ok':
            solved_problems_count += 1

    total = solved_problems_count + solved_projects_count
    percent_awesome = round((total / tasks.count()) * 100, 2)

    for project in projects:
        if project in task_to_solution:
            project.solution = task_to_solution[project]

    for problem in problems:
        if problem in task_to_solution:
            problem.solution = task_to_solution[problem]

    return render(request, "certificate.html", locals())
