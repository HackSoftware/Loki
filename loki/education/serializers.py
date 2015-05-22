from rest_framework import serializers
from .models import Student


class OnBoardingStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = (
            'studies_at',
            'works_at',
        )
