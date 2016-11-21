from test_plus.test import TestCase

from loki.hack_fmi.models import Team, TeamMembership, Competitor, Invitation, TeamMentorship
from loki.seed.factories import (TeamFactory, SeasonFactory,
                                 RoomFactory, TeamMembershipFactory,
                                 CompetitorFactory, InvitationFactory,
                                 HackFmiPartnerFactory, MentorFactory,
                                 TeamMentorshipFactory)

from faker import Factory

faker = Factory.create()


class TestTeamManager(TestCase):
    def setUp(self):
        self.active_season = SeasonFactory(is_active=True)
        self.room = RoomFactory(season=self.active_season)
        self.team = TeamFactory(season=self.active_season, room=self.room)
        self.competitor = CompetitorFactory(email=faker.email())
        self.team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                     team=self.team,
                                                     is_leader=True)

    def test_get_all_teams_for_competitor(self):
        self.assertEqual(1, Team.objects.count())
        self.assertEqual(1, Team.objects.get_all_teams_for_competitor(competitor=self.competitor).count())
        new_active_season = SeasonFactory(is_active=True)
        room = RoomFactory(season=new_active_season)
        team = TeamFactory(season=new_active_season, room=room)
        self.team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                     team=team,
                                                     is_leader=False)

        self.assertEqual(2, Team.objects.get_all_teams_for_competitor(competitor=self.competitor).count())

    def test_get_all_teams_for_competitor_if_competitor_has_no_team(self):
        competitor = CompetitorFactory(email=faker.email())
        self.assertEqual(0, Team.objects.get_all_teams_for_competitor(competitor=competitor).count())

    def test_get_all_teams_for_competitor_if_competitor_is_None(self):
        self.assertEqual(None, Team.objects.get_all_teams_for_competitor(competitor=None).first())
        self.assertEqual(0, Team.objects.get_all_teams_for_competitor(competitor=None).count())

    def test_get_all_teams_for_current_season(self):
        self.assertEqual(1, Team.objects.count())
        self.assertEqual(1, Team.objects.get_all_teams_for_current_season(season=self.active_season).count())

        room = RoomFactory(season=self.active_season)
        team = TeamFactory(season=self.active_season, room=room)
        competitor = CompetitorFactory(email=faker.email())
        self.team_membership = TeamMembershipFactory(competitor=competitor,
                                                     team=team,
                                                     is_leader=False)

        self.assertEqual(2, Team.objects.get_all_teams_for_current_season(season=self.active_season).count())

    def test_get_all_teams_for_current_season_if_no_teams(self):
        new_active_season = SeasonFactory(is_active=True)
        self.assertEqual(0, Team.objects.get_all_teams_for_current_season(season=new_active_season).count())
        self.assertEqual(None, Team.objects.get_all_teams_for_current_season(season=new_active_season).first())

    def test_get_all_teams_for_current_season_if_season_is_not_active(self):
        new_active_season = SeasonFactory(is_active=False)
        self.assertEqual(0, Team.objects.get_all_teams_for_current_season(season=new_active_season).count())
        self.assertEqual(None, Team.objects.get_all_teams_for_current_season(season=new_active_season).first())

    def test_get_all_teams_for_competitor_for_current_season(self):
        self.assertEqual(self.team, Team.objects.get_all_teams_for_current_season(season=self.active_season).
                         get_all_teams_for_competitor(competitor=self.competitor).first())

    def test_get_team_by_id(self):
        self.assertEqual(self.team, Team.objects.get_team_by_id(id=self.team.id).first())

    def test_get_team_by_id_if_id_does_not_exist(self):
        after_last_id = Team.objects.last().id + 1
        self.assertEqual(None, Team.objects.get_team_by_id(after_last_id).first())

    def test_get_team_by_name(self):
        self.assertEqual(self.team, Team.objects.get_team_by_name(name=self.team.name).first())

    def test_get_team_by_name_if_name_does_not_exist(self):
        name = faker.name()
        self.assertEqual(None, Team.objects.get_team_by_name(name=name).first())


class TestTeamMembershipManager(TestCase):
    def setUp(self):
        self.active_season = SeasonFactory(is_active=True)
        self.room = RoomFactory(season=self.active_season)
        self.team = TeamFactory(season=self.active_season, room=self.room)
        self.competitor = CompetitorFactory(email=faker.email())
        self.team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                     team=self.team,
                                                     is_leader=True)
    """
    Tests for TeamMembershipManager.
    """

    def test_list_all_teams_for_competitor(self):
        self.assertEqual(1, TeamMembership.objects.count())
        self.assertEqual([self.team], TeamMembership.objects.list_all_teams_for_competitor(competitor=self.competitor))
        new_active_season = SeasonFactory(is_active=True)
        room = RoomFactory(season=new_active_season)
        team = TeamFactory(season=new_active_season, room=room)
        self.team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                     team=team,
                                                     is_leader=False)

        self.assertEqual(team,
                         TeamMembership.objects.list_all_teams_for_competitor(competitor=self.competitor))

    def test_list_all_teams_for_competitor_if_competitor_has_no_team(self):
        competitor = CompetitorFactory(email=faker.email())
        self.assertEqual(0, TeamMembership.objects.get_all_team_memberships_for_competitor(
            competitor=competitor).count())
        self.assertEqual([], TeamMembership.objects.list_all_teams_for_competitor(competitor=competitor))

    def test_get_leader_of_team_if_competitor_is_leader(self):
        self.assertEqual(self.competitor, TeamMembership.objects.get_leader_of_team(team=self.team))

    def test_get_leader_of_team_if_team_has_no_leader(self):
        self.team_membership.is_leader = False
        self.team_membership.save()
        self.assertEqual(None, TeamMembership.objects.get_leader_of_team(team=self.team))

    def test_get_leader_of_team_if_team_is_None(self):
        self.team = None
        self.team_membership.save()
        self.assertEqual(None, TeamMembership.objects.get_leader_of_team(team=self.team))

    def test_is_competitor_leader_of_team(self):
        self.assertTrue(TeamMembership.objects.is_competitor_leader_of_team(competitor=self.competitor, team=self.team))

        self.team_membership.is_leader = False
        self.team_membership.save()
        self.assertFalse(TeamMembership.objects.is_competitor_leader_of_team(competitor=self.competitor,
                                                                             team=self.team))

    def test_is_competitor_leader_of_team_if_competitor_has_no_team(self):
        competitor = CompetitorFactory(email=faker.email())
        team = None
        self.assertFalse(TeamMembership.objects.is_competitor_leader_of_team(competitor=competitor,
                                                                             team=team))

    def test_is_competitor_leader_of_team_if_competitor_is_None(self):
        competitor = None
        self.assertFalse(TeamMembership.objects.is_competitor_leader_of_team(competitor=competitor,
                                                                             team=self.team))

    def test_is_competitor_leader(self):
        self.assertTrue(TeamMembership.objects.is_competitor_leader(competitor=self.competitor))

        self.team_membership.is_leader = False
        self.team_membership.save()
        self.assertFalse(TeamMembership.objects.is_competitor_leader(competitor=self.competitor))

    def test_is_competitor_leader_if_competitor_is_None(self):
        competitor = None
        self.assertFalse(TeamMembership.objects.is_competitor_leader(competitor=competitor))

    def test_get_leader_of_team_if_competitor_is_not_leader(self):
        self.team_membership.is_leader = False
        self.team_membership.save()
        self.assertRaises(AttributeError, TeamMembership.objects.get_leader_of_team(team=self.team))
        self.assertEqual(None, TeamMembership.objects.get_leader_of_team(team=self.team))

    """
    Tests for TeamMembershipQuerySet.
    """

    def test_get_all_team_memberships_for_competitor(self):
        self.assertEqual(self.team_membership, TeamMembership.objects.get_all_team_memberships_for_competitor(
            competitor=self.competitor).first())

    def test_get_all_team_memberships_for_competitor_if_competitor_has_no_team_membership(self):
        competitor = CompetitorFactory(email=faker.email())
        self.assertEqual(None, TeamMembership.objects.get_all_team_memberships_for_competitor(
            competitor=competitor).first())

    def test_get_all_team_memberships_for_competitor_if_competitor_is_None(self):
        competitor = None
        self.assertEqual(None, TeamMembership.objects.get_all_team_memberships_for_competitor(
            competitor=competitor).first())

    def test_get_all_team_memberships_for_team(self):
        self.assertEqual(self.team_membership, TeamMembership.objects.get_all_team_memberships_for_team(
            team=self.team).first())

    def test_get_all_team_memberships_for_competitor_with_two_teams(self):
        new_active_season = SeasonFactory(is_active=True)
        room = RoomFactory(season=new_active_season)
        team = TeamFactory(season=new_active_season, room=room)
        team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                team=team,
                                                is_leader=True)
        self.assertEqual(2, TeamMembership.objects.get_all_team_memberships_for_competitor(
            competitor=self.competitor).count())

    def test_get_all_team_memberships_for_team_if_team_has_no_team_membership(self):
        room = RoomFactory(season=self.active_season)
        team = TeamFactory(season=self.active_season, room=room)
        self.assertEqual(None, TeamMembership.objects.get_all_team_memberships_for_team(
            team=team).first())

    def test_get_all_team_memberships_for_team_if_team_is_None(self):
        team = None
        self.assertEqual(None, TeamMembership.objects.get_all_team_memberships_for_team(
            team=team).first())

    def test_get_all_team_memberships_for_team_with_two_competitors(self):
        competitor = CompetitorFactory(email=faker.email())
        team_membership = TeamMembershipFactory(competitor=competitor,
                                                team=self.team,
                                                is_leader=False)
        self.assertEqual(2, TeamMembership.objects.get_all_team_memberships_for_team(
            team=self.team).count())

    def test_get_team_membership_of_leader(self):
        self.assertEqual(self.team_membership, TeamMembership.objects.get_team_membership_of_leader(
            team=self.team).first())

    def test_get_team_membership_of_not_leader(self):
        self.team_membership.is_leader = False
        self.team_membership.save()
        self.assertEqual(None, TeamMembership.objects.get_team_membership_of_leader(
            team=self.team).first())

    def test_get_team_memberships_for_active_season(self):
        """
        get_team_memberships_for_active_season() ought to return QuerySet object.
        That's why I'm able to call .first() on it and compare the result to self.team_membership
        """
        self.assertEqual(self.team_membership, TeamMembership.objects.
                         get_team_memberships_for_active_season(competitor=self.competitor).first())

    def test_get_team_memberships_for_active_season_if_competitor_is_None(self):
        competitor = None
        self.assertEqual(None, TeamMembership.objects.
                         get_team_memberships_for_active_season(competitor=competitor).first())

    def test_get_team_membership_for_competitor_leader(self):
        self.assertEqual(self.team_membership, TeamMembership.objects.
                         get_team_membership_for_competitor_leader(competitor=self.competitor).first())

    def test_get_team_membership_for_competitor_leader_is_not_leader(self):
        self.team_membership.is_leader = False
        self.team_membership.save()
        self.assertEqual(None, TeamMembership.objects.
                         get_team_membership_for_competitor_leader(competitor=self.competitor).first())

    def test_get_team_membership_for_competitor_leader_if_competitor_is_None(self):
        self.assertEqual(None, TeamMembership.objects.
                         get_team_membership_for_competitor_leader(competitor=None).first())
        self.assertRaises(AttributeError, TeamMembership.objects.
                          get_team_membership_for_competitor_leader(competitor=None).first())


class TestTeamMentorshipManager(TestCase):
    def setUp(self):
        self.active_season = SeasonFactory(is_active=True)
        self.room = RoomFactory(season=self.active_season)
        self.team = TeamFactory(season=self.active_season, room=self.room)
        self.competitor = CompetitorFactory(email=faker.email())
        self.team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                     team=self.team,
                                                     is_leader=True)

        self.company = HackFmiPartnerFactory()
        self.mentor = MentorFactory(from_company=self.company)

        self.team_mentorship = TeamMentorshipFactory(team=self.team,
                                                     mentor=self.mentor)

    def test_get_all_team_mentorships_for_team(self):
        self.assertEqual(self.team_mentorship, TeamMentorship.objects.get_all_team_mentorships_for_team(
            team=self.team).first())

    def test_get_all_team_mentorships_for_team_with_no_mentors(self):
        room = RoomFactory(season=self.active_season)
        team = TeamFactory(season=self.active_season, room=room)
        self.assertEqual(None, TeamMentorship.objects.get_all_team_mentorships_for_team(
            team=team).first())

    def test_get_all_team_mentorships_for_none_team(self):
        self.assertEqual(None, TeamMentorship.objects.get_all_team_mentorships_for_team(
            team=None).first())


class TestCompetitorManager(TestCase):
    def setUp(self):
        self.email = faker.email()
        self.competitor = CompetitorFactory(email=self.email)

    def test_get_competitor_by_email(self):
        self.assertEqual(self.competitor, Competitor.objects.get_competitor_by_email(email=self.email).first())

    def test_get_competitor_by_wrong_email(self):
        email = faker.email()
        self.assertEqual(None, Competitor.objects.get_competitor_by_email(email=email).first())
        self.assertEqual(0, Competitor.objects.get_competitor_by_email(email=email).count())


class TestInvitationManager(TestCase):
    def setUp(self):
        self.active_season = SeasonFactory(is_active=True)
        self.room = RoomFactory(season=self.active_season)
        self.team = TeamFactory(season=self.active_season, room=self.room)
        self.leader_competitor = CompetitorFactory(email=faker.email())
        self.team_membership = TeamMembershipFactory(competitor=self.leader_competitor,
                                                     team=self.team,
                                                     is_leader=True)

        self.invited_competitor = CompetitorFactory(email=faker.email())

        self.invitaion = InvitationFactory(team=self.team, competitor=self.invited_competitor)

    def test_get_competitor_invitations_for_active_season(self):
        self.assertEqual(self.invitaion, Invitation.objects.get_competitor_invitations_for_active_season(
            competitor=self.invited_competitor).first())

    def test_cannot_get_competitor_invitations_for_inactive_season(self):
        self.active_season.is_active = False
        self.active_season.save()

        self.assertEqual(None, Invitation.objects.get_competitor_invitations_for_active_season(
            competitor=self.invited_competitor).first())

    def test_get_competitor_invitations_for_active_season_if_competitor_has_no_invitations(self):
        competitor = CompetitorFactory(email=faker.email())
        self.assertEqual(None, Invitation.objects.get_competitor_invitations_for_active_season(
            competitor=competitor).first())
