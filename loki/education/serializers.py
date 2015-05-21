from rest_framework import serializers

from hack_fmi.models import BaseUser


class BaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = (
            'email',
            'first_name',
            'last_name',
        )
        extra_kwargs = {'password': {'write_only': True}}
