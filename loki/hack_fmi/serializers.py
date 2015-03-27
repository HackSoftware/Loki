from rest_framework import serializers
from .models import Skill, Competitor


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class CompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        fields = (
            'full_name',
            'email',
            'is_vegetarian',
            'known_skills',
            'faculty_number',
            'shirt_size',
            'password'
        )
