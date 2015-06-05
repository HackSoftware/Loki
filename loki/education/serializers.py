from rest_framework import serializers
from .models import Student, Course, CourseAssignment


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'name',
            'start_time',
            'end_time',
            'url',
        )


class StudentSerializer(serializers.ModelSerializer):

    courses = CourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = (
            'studies_at',
            'works_at',
            'courses',
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
