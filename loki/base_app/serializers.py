from rest_framework import serializers, generics
from base_app.models import Event, Ticket
from education.serializers import StudentSerializer, TeacherSerializer

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
            'studies_at',
            'works_at'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'start_date',
            'url'
        )


class TicketSerializer(serializers.ModelSerializer):
    base_user = BaseUserSerializer(many=False, read_only=True)
    event = EventSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'event',
            'base_user'
        )


class BaseUserMeSerializer(serializers.ModelSerializer):
    competitor = CompetitorSerializer(many=False, read_only=True)
    student = StudentSerializer(many=False, read_only=True)
    teacher = TeacherSerializer(many=False, read_only=True)
    ticket_set = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = BaseUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'avatar',
            'github_account',
            'linkedin_account',
            'twitter_account',
            'competitor',
            'student',
            'teacher',
            'ticket_set',
            'works_at',
            'studies_at',
        )


class UpdateBaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = (
            'first_name',
            'last_name',
            'avatar',
            'full_image',
            'github_account',
            'linkedin_account',
            'twitter_account',
            'works_at',
            'studies_at',
        )
