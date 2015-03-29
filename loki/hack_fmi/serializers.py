from rest_framework import serializers

from .models import Skill, Competitor, Team, TeamMembership


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class CompetitorSerializer(serializers.ModelSerializer):
    known_skills = SkillSerializer(many=True, read_only=True)

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


# class TeamMembershipSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TeamMembership
#         fields = (
#             'competitor',
#             'team',
#             'is_leader',
#         )
