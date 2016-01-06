import requests
from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from base_app.models import Company, City
from .models import (Lecture, CheckIn, Course, Student, Solution,
                     CourseAssignment, StudentNote, Teacher, WorkingAt, Task, Certificate)
from .helper import generate_grader_headers


class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certificate
        fields = ('id',)


class SolutionStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = ('status', 'test_output', 'return_code')

    def get_status(self, obj):
        path = '/check_result/{}/'.format(obj.build_id)
        req_and_resource = "GET {}".format(path)

        headers = generate_grader_headers(path, req_and_resource)
        url = obj.check_status_location

        r = requests.get(url, headers=headers)

        if r.status_code == 204:
            obj.status = Solution.PENDING
        elif r.status_code == 200:
            if r.json()['result_status'] == 'ok':
                obj.status = Solution.OK
            elif r.json()['result_status'] == 'not_ok':
                obj.status = Solution.NOT_OK
            obj.test_output = r.json()['output']
            obj.return_code = r.json()['returncode']

        obj.save()

        return obj.get_status()


class SolutionSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    task = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=Task.objects.all(),
    )

    class Meta:
        model = Solution
        extra_kwargs = {'url': {'required': False}}
        fields = ('id', 'task', 'url', 'code', 'status',
                  'test_output', 'return_code', 'created_at')

    def get_status(self, obj):
        return obj.get_status()

    def validate_url(self, url):
        self.solution_url = url

        if self.solution_url is not None:
            # Check if url is valid
            val = URLValidator()
            try:
                val(self.solution_url)
            except ValidationError:
                raise serializers.ValidationError('Въведете валиден GitHub URL адрес.')

            github_domain = "github.com"
            splitted_url = self.solution_url.split("/")
            file_name = splitted_url[-1]

            # Check if the url has github domain and ends with fail extension
            if github_domain not in splitted_url:
                raise serializers.ValidationError('Въведете валиден GitHub URL адрес.')
            if "." not in file_name:
                raise serializers.ValidationError('Въведете валиден GitHub URL адрес.')
            elif len(file_name) <= file_name.index(".") + 1:
                raise serializers.ValidationError('Въведете валиден GitHub URL адрес.')

        return self.solution_url


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'description', 'name', 'week')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class NoteTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'first_name',
            'last_name',
        )


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id', 'date',)


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = ('id', 'date', 'student')


class TeacherSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = (
            'first_name',
            'last_name',
            'email',
            'avatar',
            'github_account',
            'linkedin_account',
            'twitter_account'
        )


class StudentNoteSerializer(serializers.ModelSerializer):
    author = TeacherSetSerializer(many=False, read_only=True)

    class Meta:
        model = StudentNote
        fields = ('text', 'assignment', 'post_time', 'author')


class CourseSerializer(serializers.ModelSerializer):
    teacher_set = TeacherSetSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'start_time',
            'end_time',
            'teacher_set',
            'fb_group',
            'url',
        )


class CourseAssignmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False, read_only=True)
    certificate = CertificateSerializer(read_only=True)

    class Meta:
        model = CourseAssignment
        fields = (
            'id',
            'is_attending',
            'is_online',
            'course',
            'certificate',
        )


class SingleStudent(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'studies_at',
            'works_at',
            'github_account',
            'linkedin_account',
            'mac',
        )


class FullCASerializer(serializers.ModelSerializer):
    user = SingleStudent(many=False, read_only=True)
    studentnote_set = StudentNoteSerializer(many=True, read_only=True)

    class Meta:
        model = CourseAssignment
        fields = (
            'id',
            'is_attending',
            'student_presence',
            'user',
            'studentnote_set',
        )


class WorkingAtSerializer(serializers.HyperlinkedModelSerializer):
    location = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=City.objects.all(),
    )

    location_full = CitySerializer(
        many=False,
        read_only=True,
        source='location',
    )

    course = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=Course.objects.all(),
        allow_null=True,
    )

    course_full = CourseSerializer(
        many=False,
        read_only=True,
        source='course',
        required=False,
    )

    company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = WorkingAt
        fields = (
            'id',
            'company',
            'company_name',
            'course',
            'course_full',
            'location',
            'location_full',
            'came_working',
            'start_date',
            'end_date',
            'title',
            'description',
        )

    def create(self, validated_data):
        return WorkingAt.objects.create(**validated_data)


class StudentSerializer(serializers.ModelSerializer):
    courseassignment_set = CourseAssignmentSerializer(many=True, read_only=True)
    workingat_set = WorkingAtSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = (
            'id',
            'studies_at',
            'works_at',
            'courseassignment_set',
            'github_account',
            'linkedin_account',
            'mac',
            'workingat_set'
        )


class StudentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'id',
            'first_name',
            'last_name',
            'github_account',
            'studies_at',
            'works_at',
            'avatar',
        )


class OnBoardingStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'studies_at',
            'works_at',
        )


class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'studies_at',
            'works_at',
            'mac',
        )


class TeacherSerializer(serializers.ModelSerializer):
    teached_courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = (
            'phone',
            'mac',
            'teached_courses',
        )
