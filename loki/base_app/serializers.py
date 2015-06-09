from rest_framework import serializers, generics
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
    competitor = CompetitorSerializer(many=False, read_only=True)
    student = StudentSerializer(many=False, read_only=True)

    class Meta:
        model = BaseUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'github_account',
            'linkedin_account',
            'twitter_account',
            'competitor',
            'student',
        )


class UpdateBaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = (
            'first_name',
            'last_name',
            'github_account',
            'linkedin_account',
            'twitter_account',
        )
