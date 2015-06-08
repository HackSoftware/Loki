from rest_framework import serializers

from .models import Lecture, CheckIn


class LectureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = ('date',)


class CheckInSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckIn
        fields = ('date', 'student')
