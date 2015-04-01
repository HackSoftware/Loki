from rest_framework import serializers

from .models import Skill, Competitor, Team, TeamMembership, Season, Invitation


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
    known_skills = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Skill.objects.all())
    teammembership_set = TeamMembershipSerializer(many=True, read_only=True)

    class Meta:
        model = Competitor
        fields = (
            'email',
            'first_name',
            'last_name',
            'is_vegetarian',
            'known_skills',
            'faculty_number',
            'shirt_size',
            'password',
            'teammembership_set',
            'needs_work',

        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        new_user = super().create(validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user


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

    def create(self, validated_data):
        team = super(TeamSerializer, self).create(validated_data)
        # Implement season logic here
        season = Season.objects.all()
        team.season = season[0]
        team.save()
        return team


class InvitationSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=False, read_only=True)

    class Meta:
        model = Invitation
        fields = (
            'team',
            'competitor',
        )
