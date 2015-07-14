from rest_framework import serializers
from base_app.models import Company, City

from .models import (Lecture, CheckIn, Course, Student,
                     CourseAssignment, StudentNote, Teacher, WorkingAt)


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


class StudentNoteSerializer(serializers.ModelSerializer):
    author = NoteTeacherSerializer(many=False, read_only=True)

    class Meta:
        model = StudentNote
        fields = (
            'text',
            'author',
            'post_time',
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

    class Meta:
        model = CourseAssignment
        fields = (
            'is_attending',
            'is_online',
            'course',
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

    course_assignment = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=CourseAssignment.objects.all(),
    )

    course_assignment_full = CourseAssignmentSerializer(
        many=False,
        read_only=True,
        source='course_assignment',
    )

    company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = WorkingAt
        fields = (
            'id',
            'company',
            'company_name',
            'course_assignment',
            'course_assignment_full',
            'location',
            'location_full',
            'came_working',
            'start_date',
            'end_date',
            'title',
            'description',
        )


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
