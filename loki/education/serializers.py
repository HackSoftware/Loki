from rest_framework import serializers
from hack_fmi.models import BaseUser

from .models import Lecture, CheckIn, Course, Student, CourseAssignment, StudentNote, Teacher, Company


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


class StudentSerializer(serializers.ModelSerializer):

    courseassignment_set = CourseAssignmentSerializer(many=True, read_only=True)

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


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('name',)
