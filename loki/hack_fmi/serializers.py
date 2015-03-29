from rest_framework import serializers

from .models import Skill, Competitor, Team, TeamMembership


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class TeamMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembership
        fields = (
            'competitor',
            'team',
            'is_leader',
        )


class CompetitorSerializer(serializers.ModelSerializer):
    known_skills = SkillSerializer(many=True, read_only=True)
    teammembership_set = TeamMembershipSerializer(many=True, read_only=True)

    class Meta:
        model = Competitor
        fields = (
            'email',
            'full_name',
            'is_vegetarian',
            'known_skills',
            'faculty_number',
            'shirt_size',
            'password',
            'teammembership_set'
        )
        extra_kwargs = {'password': {'write_only': True}}


class TeamSerializer(serializers.ModelSerializer):
    members = CompetitorSerializer(many=True, read_only=True)
    technologies = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = (
            'name',
            'members',
            'idea_description',
            'repository',
            'technologies',
        )
