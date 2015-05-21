from rest_framework import serializers

from hack_fmi.models import BaseUser


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
