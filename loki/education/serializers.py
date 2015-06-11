from rest_framework import serializers

from .models import Lecture, CheckIn, Course


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
        fields = ('id', 'name')
