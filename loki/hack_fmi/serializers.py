from rest_framework import serializers

from .models import Skill, Competitor, Team, TeamMembership, Season, Invitation, Mentor, TeamMentorship


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


class CompetitorInTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competitor
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
        )


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


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name')


class PublicCompetiorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competitor
        fields = (
            'first_name',
            'last_name',
        )


class MentorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentor
        fields = (
            'id',
            'name',
            'description',
            'picture',
        )


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

    room = serializers.StringRelatedField()

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


class TeamSerializer(serializers.ModelSerializer):
    members = CompetitorInTeamSerializer(many=True, read_only=True)
    leader_id = serializers.SerializerMethodField()
    room = serializers.StringRelatedField()

    def get_leader_id(self, obj):
        leader_membership = TeamMembership.objects.get_team_membership_of_leader(team=obj)
        if leader_membership:
            return leader_membership.first().team.get_leader().id

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
            'idea_description',
            'repository',
            'technologies',
            'technologies_full',
            'need_more_members',
            'members_needed_desc',
            'room',
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
        competitor = Competitor.objects.filter(email=data['competitor_email'])

        if Invitation.objects.filter(competitor=competitor).count() > 0:
            raise serializers.ValidationError("You have already sent a an invitation for that user!")

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

        competitor = Competitor(**validated_data)
        competitor.baseuser_ptr_id = self.baseuser.id
        competitor.__dict__.update(self.baseuser.__dict__)
        competitor.save()
        competitor.known_skills = known_skills
        return competitor

    class Meta:
        model = Competitor

        known_skills = serializers.PrimaryKeyRelatedField(
            queryset=Skill.objects.all(),
            many=True,
            read_only=False
        )

        fields = (
            'is_vegetarian',
            'shirt_size',
            'needs_work',
            'social_links',
            'known_skills',
        )
