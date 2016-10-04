from rest_framework import serializers

from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):

    date = serializers.DateField(format="%d %B %Y")
    start_time = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Interview
        fields = ('id', 'date', 'start_time')
