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

from ..permissions import IsTeacher, IsTeacherForCA
from ..models import (CheckIn, Student, Lecture, CourseAssignment, WorkingAt,
                      Task, Solution, Certificate, Teacher)

from ..serializers import (LectureSerializer, CourseSerializer, FullCASerializer,
                           SolutionSerializer, WorkingAtSerializer,
                           CitySerializer, CompanySerializer, TaskSerializer, StudentNoteSerializer,
                           SolutionStatusSerializer)
from ..tasks import submit_solution
from ..mixins import SolutionApiAuthenticationPermissionMixin


@csrf_exempt
@require_POST
def set_check_in(request):
    mac = request.POST['mac']
    token = request.POST['token']

    if settings.CHECKIN_TOKEN != token:
        return HttpResponse(status=511)

    try:
        student = Student.objects.filter(mac__iexact=mac).first()
        teacher = Teacher.objects.filter(mac__iexact=mac).first()
        if student:
            student_check = CheckIn.objects.create(mac=mac, user=student)
            student_check.save()
        if teacher:
            teacher_check = CheckIn.objects.create(mac=mac, user=teacher)
            teacher_check.save()
        if not student and not teacher:
            anonymous_user_check = CheckIn.objects.create(mac=mac, user=None)
            anonymous_user_check.save()
    except IntegrityError:
        return HttpResponse(status=418)

    return HttpResponse(status=200)


class SolutionStatusAPI(
        SolutionApiAuthenticationPermissionMixin,
        mixins.RetrieveModelMixin,
        generics.GenericAPIView):
    model = Solution
    serializer_class = SolutionStatusSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_queryset(self):
        student = self.request.user.get_student()
        return student.solution_set


class SolutionsAPI(
        SolutionApiAuthenticationPermissionMixin,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        generics.GenericAPIView):
    model = Solution
    serializer_class = SolutionSerializer
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
