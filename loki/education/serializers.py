from rest_framework import serializers

from .models import Lecture, CheckIn, Course, Student, CourseAssignment


class LectureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = ('id', 'date',)


class CheckInSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckIn
        fields = ('id', 'date', 'student')


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'start_time',
            'end_time',
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


class StudentSerializer(serializers.ModelSerializer):

    courseassignment_set = CourseAssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = (
            'studies_at',
            'works_at',
            'courseassignment_set',
            'github_account',
            'linkedin_account',
            'mac',
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
            'mac'
        )


class TeacherSerializer(serializers.ModelSerializer):

    teached_courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = (
            'phone',
            'mac',
            'teached_courses',
        )
