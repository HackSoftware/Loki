from rest_framework import serializers
from education.serializers import StudentSerializer

from hack_fmi.models import BaseUser
from hack_fmi.serializers import CompetitorSerializer


class BaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class BaseUserMeSerializer(serializers.ModelSerializer):
    competitor = CompetitorSerializer(many=False)
    student = StudentSerializer(many=False)

    class Meta:
        model = BaseUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'competitor',
            'student'
        )
