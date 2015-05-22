from rest_framework import serializers

from .models import Skill, Competitor, Team, TeamMembership, Season, Invitation, Mentor


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


class PublicCompetiorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competitor
        fields = (
            'first_name',
            'last_name',
        )


class CompetitorSerializer(serializers.ModelSerializer):
    known_skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        read_only=False
    )

    teammembership_set = serializers.SerializerMethodField('get_active_teams')

    def get_active_teams(self, obj):
        team_membership_query_set = TeamMembership.objects.filter(
            team__season__is_active=True,
            competitor=obj
        )

        serializer = TeamMembershipSerializer(
            instance=team_membership_query_set,
            many=True, context=self.context
        )
        return serializer.data

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
            'team_set',
            'needs_work',
            'social_links',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        new_user = super().create(validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user


class MentorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentor
        fields = (
            'id',
            'name',
            'description',
            'picture',
        )


class TeamSerializer(serializers.ModelSerializer):
    members = CompetitorSerializer(many=True, read_only=True)
    technologies = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Skill.objects.all()
    )

    technologies_full = SkillSerializer(
        many=True,
        read_only=True,
        source='technologies',
    )

    mentors = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Mentor.objects.all(),
        required=False,
    )

    mentors_full = MentorSerializer(
        many=True,
        read_only=True,
        source='mentors',
    )

    room = serializers.StringRelatedField()

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'members',
            'idea_description',
            'repository',
            'technologies',
            'technologies_full',
            'mentors',
            'mentors_full',
            'need_more_members',
            'members_needed_desc',
            'room',
            'picture',
        )

    def validate(self, data):
        """
         Check that number of mentors is less than allowed.
        """
        season = Season.objects.get(is_active=True)
        if any('mentors' in key for key in data):
            if data['mentors'] > season.max_mentor_pick:
                raise serializers.ValidationError("You are not allowed to pick that much mentors")
        return data


class PublicTeamSerializer(serializers.ModelSerializer):
    members = PublicCompetiorSerializer(many=True, read_only=True)
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
            'members',
            'idea_description',
            'repository',
            'technologies',
            'technologies_full',
            'mentors',
            'need_more_members',
            'members_needed_desc',
            'room',
            'picture',
        )


class InvitationSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=False, read_only=True)

    class Meta:
        model = Invitation
        fields = (
            'id',
            'team',
            'competitor',
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


class OnBoardingCompetitorSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.baseuser = kwargs.pop('baseuser')

        super(OnBoardingCompetitorSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        competitor = Competitor(**validated_data)
        competitor.baseuser_ptr_id = self.baseuser.id
        competitor.save()
        competitor.__dict__.update(self.baseuser.__dict__)
        competitor.save()
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
