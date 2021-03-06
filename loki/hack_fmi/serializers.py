from rest_framework import serializers

from .models import (Skill, Competitor, Team, TeamMembership,
                     Season, Invitation, Mentor, TeamMentorship,
                     SeasonCompetitorInfo)


class TeamMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembership
        fields = (
            'id',
            'competitor',
            'team',
            'is_leader',
        )


class CompetitorSerializer(serializers.ModelSerializer):
    known_skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        read_only=False
    )

    current_teammembership_set = serializers.SerializerMethodField('get_active_teams')
    teammembership_set = TeamMembershipSerializer(many=True, read_only=True)

    def get_active_teams(self, obj):
        team_membership_query_set = TeamMembership.objects.get_team_memberships_for_active_season(competitor=obj)

        serializer = TeamMembershipSerializer(
            instance=team_membership_query_set,
            many=True, context=self.context
        )
        return serializer.data

    class Meta:
        model = Competitor
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'is_vegetarian',
            'known_skills',
            'faculty_number',
            'shirt_size',
            'password',
            'current_teammembership_set',
            'teammembership_set',
            'needs_work',
            'social_links',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        new_user = super().create(validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name')


class CompetitorInTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competitor
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
        )


class CompetitorListSerializer(CompetitorInTeamSerializer):
    known_skills_full = SkillSerializer(
        many=True,
        read_only=True,
        source='known_skills',
    )

    class Meta(CompetitorInTeamSerializer.Meta):
        model = Competitor
        fields = CompetitorInTeamSerializer.Meta.fields + ('known_skills_full',
                                                           'other_skills')


class CustomTeamSerializer(serializers.ModelSerializer):
    members = CompetitorInTeamSerializer(many=True, read_only=True)
    leader_id = serializers.SerializerMethodField()

    def get_leader_id(self, obj):
        leader_membership = TeamMembership.objects.get_team_membership_of_leader(team=obj)
        if leader_membership:
            return leader_membership.first().team.get_leader().id

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'members',
            'season',
            'leader_id'
        )


class PublicCompetiorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competitor
        fields = (
            'first_name',
            'last_name',
        )


class TeamWithRoomSerializer(serializers.ModelSerializer):
    room = serializers.ReadOnlyField(source='get_room', allow_null=True)

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'room',
        )


class MentorSerializer(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField()

    def get_teams(self, obj):
        mentor_teams = obj.team_set.all()
        serializer = TeamWithRoomSerializer(mentor_teams, many=True)
        return serializer.data

    class Meta:
        model = Mentor
        fields = (
            'id',
            'name',
            'description',
            'picture',
            'teams',
        )


class MentorForTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentor
        fields = ('id', )


class SeasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Season
        fields = (
            'id',
            'name',
            'topic',
            'front_page',
            'min_team_members_count',
            'max_team_members_count',
            'sign_up_deadline',
            'mentor_pick_start_date',
            'mentor_pick_end_date',
            'make_team_dead_line'
        )


class PublicTeamSerializer(serializers.ModelSerializer):
    technologies_full = SkillSerializer(
        many=True,
        read_only=True,
        source='technologies',
    )

    room = serializers.ReadOnlyField(source='get_room', allow_null=True)

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'idea_description',
            'repository',
            'technologies_full',
            'need_more_members',
            'members_needed_desc',
            'room',
            'place'
        )


class TeamMentorshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamMentorship
        fields = (
            'team',
            'mentor',
        )
        read_only_fields = ('team',)


class TeamSerializer(serializers.ModelSerializer):
    members = CompetitorInTeamSerializer(many=True, read_only=True)
    leader_id = serializers.SerializerMethodField()
    leader_email = serializers.SerializerMethodField()
    room = serializers.ReadOnlyField(source='get_room', allow_null=True)

    def get_leader_id(self, obj):
        leader_membership = TeamMembership.objects.get_team_membership_of_leader(team=obj)
        if leader_membership:
            return leader_membership.first().team.get_leader().id

    def get_leader_email(self, obj):
        leader_membership = TeamMembership.objects.get_team_membership_of_leader(team=obj)
        if leader_membership:
            return leader_membership.first().team.get_leader().email

    technologies_full = SkillSerializer(
        many=True,
        read_only=True,
        source='technologies',
    )

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'members',
            'leader_id',
            'leader_email',
            'idea_description',
            'repository',
            'technologies',
            'technologies_full',
            'need_more_members',
            'members_needed_desc',
            'room',
            'updated_room',
            'place',
        )


class InvitationTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            'id',
            'name'
        )


class InvitationSerializer(serializers.ModelSerializer):
    team = InvitationTeamSerializer(read_only=True)
    competitor_email = serializers.EmailField(required=True, write_only=True)
    competitor = CompetitorSerializer(required=False)

    class Meta:
        model = Invitation
        fields = (
            'id',
            'team',
            'competitor_email',
            'competitor'
        )

    def validate(self, data):
        competitor_email = data.pop('competitor_email')
        competitor = Competitor.objects.get(email=competitor_email)
        data['competitor'] = competitor

        return data


class OnBoardingCompetitorSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.baseuser = kwargs.pop('baseuser')

        super(OnBoardingCompetitorSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        # TODO: Find a better way to do this
        known_skills = validated_data.pop("known_skills")
        other_skills = validated_data.pop("other_skills")

        competitor = Competitor(**validated_data)
        competitor.baseuser_ptr_id = self.baseuser.id
        competitor.__dict__.update(self.baseuser.__dict__)
        competitor.save()
        competitor.known_skills = known_skills
        competitor.other_skills = other_skills
        return competitor

    class Meta:
        model = Competitor

        known_skills = serializers.PrimaryKeyRelatedField(
            queryset=Skill.objects.all(),
            many=True,
            read_only=False
        )

        fields = (
            'id',
            'is_vegetarian',
            'shirt_size',
            'needs_work',
            'social_links',
            'known_skills',
            'other_skills'
        )


class SeasonCompetitorInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SeasonCompetitorInfo

        fields = (
            'competitor',
            'season',
            'looking_for_team'
        )

        extra_kwargs = {
            'competitor': {
                'write_only': True
            },
            'season': {
                'write_only': True
            }
        }
