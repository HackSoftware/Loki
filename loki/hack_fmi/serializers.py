from rest_framework import serializers
from .models import Language, Competitor


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name',)


class CompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        fields = (
            'first_name',
            'last_name',
            'email',
            'known_technologies',
            'faculty_number',
            'shirt_size',
            'password'
        )
