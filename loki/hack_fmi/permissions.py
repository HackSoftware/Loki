from rest_framework import permissions
from datetime import date

from .models import (Team, Competitor, TeamMembership,
                     Season, TeamMentorship, BlackListToken)


class IsHackFMIUser(permissions.BasePermission):
    message = "You are not a member of the HackFMI system!"

    def has_permission(self, request, view):
        is_hackfmi_user = request.user.get_competitor()
        return request.user and is_hackfmi_user


class IsTeamLeaderOrReadOnly(permissions.BasePermission):
    message = "You are not a leader of this team!"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.get_leader() == request.user.get_competitor()


class IsTeamLeader(permissions.BasePermission):
    message = "You are not a leader of this team!"

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'DELETE':

            competitor = request.user.get_competitor()
            team = TeamMembership.objects.get_team_memberships_for_active_season(
                competitor=competitor).first().team
            return TeamMembership.objects.is_competitor_leader_of_team(competitor=competitor, team=team)

        return True

    def has_object_permission(self, request, view, obj):
        if request.method != 'POST':
            return obj.team.get_leader() == request.user.get_competitor()

        return True


class IsMemberOfTeam(permissions.BasePermission):
    message = "You are not a member of this team!"

    def has_object_permission(self, request, view, obj):
        return obj.competitor == request.user.get_competitor()


class IsTeamMembershipInActiveSeason(permissions.BasePermission):
    message = "This team is not in an active season!"

    def has_object_permission(self, request, view, obj):
        return obj.team.season.is_active is True


class IsSeasonDeadlineUpToDate(permissions.BasePermission):
    message = "The deadline for creating new teams has expired!"

    def has_permission(self, request, view):
        if request.method == "POST":
            active_season = Season.objects.get(is_active=True)
            return active_season.make_team_dead_line > date.today()
        return True


class IsMentorDatePickUpToDate(permissions.BasePermission):
    message = "Mentors pick period hasn't started yet or is over."

    def has_permission(self, request, view):
        if not request.data:
            return True
        today = date.today()
        team = TeamMembership.objects.get_team_memberships_for_active_season(
            competitor=request.user.get_competitor()).first().team
        return team.season.mentor_pick_start_date <= today and team.season.mentor_pick_end_date >= today


class CanAttachMoreMentorsToTeam(permissions.BasePermission):
    message = "You've reached the max limit of mentors for you team."

    def has_permission(self, request, view):
        if request.method == 'POST':
            team = TeamMembership.objects.get_team_memberships_for_active_season(
                competitor=request.user.get_competitor()).first().team
            max_mentors_pick = team.season.max_mentor_pick
            mentors_for_current_team = TeamMentorship.objects.get_all_team_mentorships_for_team(team=team).count()
            return max_mentors_pick > mentors_for_current_team
        # If request.method = 'DELETE'
        return True


class CantAttachMentorThatIsAlreadyAttachedToTeam(permissions.BasePermission):
    message = "This mentor is already assigned to team!"

    def has_permission(self, request, view):
        if request.method == 'POST':
            return not TeamMentorship.objects.filter(mentor__id=request.data['mentor'], team__season__is_active=True)
        return True


class MentorIsAlreadySelectedByThisTeamLeader(permissions.BasePermission):
    message = "You already selected this mentor."

    def has_permission(self, request, view):
        if request.method == 'POST':
            team = TeamMembership.objects.get_team_memberships_for_active_season(
                competitor=request.user.get_competitor()).first().team
            return not TeamMentorship.objects.filter(mentor__id=request.data['mentor'],
                                                     team__season__is_active=True, team=team)
        return True


class CantCreateTeamWithTeamNameThatAlreadyExists(permissions.BasePermission):
    message = "A team with that name already exists!"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        """
        We check whether a team with that name alredy exists when we register or change a team
        (POST and PATCH), otherwise we return True.
        """
        new_name_of_team = request.data.get('name') if request.data.get('name') else None

        if request.method == "PATCH" and new_name_of_team and new_name_of_team != view.get_object().name:
            qs = Team.objects.get_team_by_name_for_active_season(name=new_name_of_team)
            return not qs.exists()

        if request.method == "POST":
            qs = Team.objects.get_team_by_name_for_active_season(name=new_name_of_team)
            return not qs.exists()

        return True


class TeamLeaderCantCreateOtherTeam(permissions.BasePermission):
    message = "You are a teamleader and cannot register another team!"

    def has_permission(self, request, view):
        if request.method == "POST":
            user = request.user.get_competitor()
            return not TeamMembership.objects.is_competitor_leader_in_current_season(competitor=user)
        """
        TeamLeaders cant send POST queries in order to register another team, since they have their own one.
        TeamLeaders can only change and see their own teams(GET and PATCH queries return True)
        """
        return True


class IsTeamleaderOrCantCreateIvitation(permissions.BasePermission):
    message = "Only current season team leaders can invite members."

    def has_permission(self, request, view):
        if request.method == "POST":
            user = request.user.get_competitor()
            return TeamMembership.objects.is_competitor_leader_in_current_season(competitor=user)

        """
        Return True if you just want to see all the invitations without creating a new invitation.
        """
        return True


class IsInvitedMemberAlreadyInYourTeam(permissions.BasePermission):

    message = "The member you are trying to add is already in your team!"

    def has_permission(self, request, view):
        if request.method == "POST":
            leader_team = TeamMembership.objects.\
                get_team_memberships_for_active_season(competitor=request.user.get_competitor()).first().team
            competitor = Competitor.objects.get_competitor_by_email(email=request.data['competitor_email'])
            return not TeamMembership.objects.\
                get_team_memberships_for_active_season(competitor=competitor).\
                get_all_team_memberships_for_team(team=leader_team).exists()
        """
        Return True if you just want to see all the invitations without creating a new invitation.
        """
        return True


class IsInvitedMemberAlreadyInOtherTeam(permissions.BasePermission):

    message = "This competitor is already member of a team!"

    def has_permission(self, request, view):
        if request.method == "POST":
            competitor = Competitor.objects.get_competitor_by_email(email=request.data['competitor_email'])
            return TeamMembership.objects.get_team_memberships_for_active_season(competitor=competitor).count() == 0

        """
        Return True if you just want to see all the invitations without creating a new invitation.
        """
        return True


class CanInviteMoreMembersInTeam(permissions.BasePermission):

    def __getattr__(self, name):
        """
        Since https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/views.py#L320
        is calling getattr and we want to have a good message with the max number of mentors
        We redefine __getattr__ to return the proper message when getattr(permission, 'message', None) is called.
        This is bad design from DRF.
        """
        if name == 'message':
            active_season = Season.objects.get(is_active=True)

            message = "You cannot invite more than {} in your team".format(active_season.max_team_members_count)
            return message

        return object.__getattribute__(self, name)

    def has_permission(self, request, view):
        if request.method == "POST":
            team = TeamMembership.objects.get_team_memberships_for_active_season(
                competitor=request.user.get_competitor()).first().team
            # user_team = TeamMembership.objects.get(competitor=request.user.get_competitor()).team
            members_in_team = TeamMembership.objects.get_all_team_memberships_for_team(team=team).count()

            return members_in_team < team.season.max_team_members_count

        """
        Return True if you just want to see all the invitations without creating a new invitation.
        """
        return True


class CanNotAccessWronglyDedicatedIvitation(permissions.BasePermission):

    message = "This invitation is not dedicated to you!"

    def has_object_permission(self, request, view, obj):
        return request.user.get_competitor() == obj.competitor


class IsInvitedUserInTeam(permissions.BasePermission):

    message = "You are already a member of another team!"

    def has_object_permission(self, request, view, obj):
        return not TeamMembership.objects.\
            get_team_memberships_for_active_season(competitor=request.user.get_competitor()).exists()


class CanNotAcceptInvitationIfTeamLeader(permissions.BasePermission):

    message = "You are a leader of a team and cannot accept any invitations!"

    def has_object_permission(self, request, view, obj):
        competitor = request.user.get_competitor()
        return not TeamMembership.objects.is_competitor_leader_in_current_season(competitor=competitor)


class IsInvitedMemberCompetitor(permissions.BasePermission):

    message = "Competitor with this email does not exist!"

    def has_permission(self, request, view):
        if request.method == "POST":
            return Competitor.objects.get_competitor_by_email(email=request.data['competitor_email']).exists()
        return True


class IsSeasonActive(permissions.BasePermission):
    message = "You cannot post data in nonactive season!"

    def has_permission(self, request, view):
        if request.method == 'POST':
            season = Season.objects.filter(id=request.data['season']).first()

            if season is not None:
                return season.is_active

        return True


class IsCompetitorMemberOfTeamForActiveSeason(permissions.BasePermission):
    message = "You are already member of team in this season!"

    def has_permission(self, request, view):
        if request.method == 'POST':
            competitor = Competitor.objects.filter(id=request.data['competitor']).first()

            if competitor is not None:
                return not TeamMembership.objects.get_team_memberships_for_active_season(
                    competitor=competitor).exists()

        return True


class IsJWTTokenBlackListed(permissions.BasePermission):

    message = "Signature has expired."

    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION', False)

        return not BlackListToken.objects.filter(token=token).exists()


class CantChangeOtherCompetitorsData(permissions.BasePermission):

    message = "You cannot change other competitor's info."

    def has_object_permission(self, request, view, obj):
        return request.user.get_competitor() == obj.competitor
