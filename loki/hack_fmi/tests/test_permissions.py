from test_plus.test import TestCase
from loki.common.utils import make_mock_object
from loki.seed.factories import (BaseUserFactory, CompetitorFactory, TeamFactory,
                                 TeamMembershipFactory)
from loki.hack_fmi.permissions import IsHackFMIUser, IsTeamLeaderOrReadOnly, IsTeamLeader


class HackFMIUserTest(TestCase):

    def setUp(self):
        self.permission = IsHackFMIUser()

    def test_non_hackfmi_user_can_not_access(self):
        user = BaseUserFactory()
        request = make_mock_object(user=user)
        self.assertFalse(self.permission.has_permission(request=request, view=None))

    def test_hackfmi_user_can__access(self):
        user = CompetitorFactory()
        request = make_mock_object(user=user)
        self.assertTrue(self.permission.has_permission(request=request, view=None))


class IsTeamLeaderOrReadOnlyTest(TestCase):
    def setUp(self):
        self.permission = IsTeamLeaderOrReadOnly()
        self.team = TeamFactory()
        self.competitor = CompetitorFactory()
        self.team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                     team=self.team,
                                                     is_leader=False)

    def test_non_team_leader_can_read(self):
        request = make_mock_object(user=self.competitor, method='GET')
        self.assertTrue(self.permission.has_object_permission(request=request, view=None, obj=self.team))

    def test_non_team_leader_can_not_delete_team(self):
        request = make_mock_object(user=self.competitor, method='DELETE')
        self.assertFalse(self.permission.has_object_permission(request=request, view=None, obj=self.team))

    def test_non_team_leader_can_not_update_team(self):
        request = make_mock_object(user=self.competitor, method='PATCH')
        self.assertFalse(self.permission.has_object_permission(request=request, view=None, obj=self.team))

    def test_team_leader_can_read(self):
        self.team_membership.is_leader = True
        self.team_membership.save()

        request = make_mock_object(user=self.competitor, method='GET')
        self.assertTrue(self.permission.has_object_permission(request=request, view=None, obj=self.team))

    def test_team_leader_can_delete_team(self):
        self.team_membership.is_leader = True
        self.team_membership.save()

        request = make_mock_object(user=self.competitor, method='DELETE')
        self.assertTrue(self.permission.has_object_permission(request=request, view=None, obj=self.team))

    def test_team_leader_can_update_team(self):
        self.team_membership.is_leader = True
        self.team_membership.save()

        request = make_mock_object(user=self.competitor, method='PATCH')
        self.assertTrue(self.permission.has_object_permission(request=request, view=None, obj=self.team))


class IsTeamLeaderTest(TestCase):
    def setUp(self):
        self.permission = IsTeamLeader()
        self.team = TeamFactory(season__is_active=True)
        self.competitor = CompetitorFactory()
        self.team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                     team=self.team,
                                                     is_leader=False)

    def test_non_leader_can_not_send_post_request(self):
        data = {'team': self.team}
        request = make_mock_object(user=self.competitor, method='POST', data=data)
        self.assertFalse(self.permission.has_permission(request=request, view=None))

    def test_non_leader_can_get_view(self):
        request = make_mock_object(user=self.competitor, method='GET')
        self.assertTrue(self.permission.has_permission(request=request, view=None))

    def test_non_leader_can_send_post_request(self):
        request = make_mock_object(user=self.competitor, method='POST')
        self.assertTrue(self.permission.has_object_permission(request=request, view=None, obj=self.team_membership))

    def test_non_leader_can_not_send_get_request(self):
        request = make_mock_object(user=self.competitor, method='GET')
        self.assertFalse(self.permission.has_object_permission(request=request, view=None, obj=self.team_membership))

    def test_non_leader_can_not_delete(self):
        request = make_mock_object(user=self.competitor, method='DELETE')
        self.assertFalse(self.permission.has_object_permission(request=request, view=None, obj=self.team_membership))

    def test_leader_can_delete(self):
        self.team_membership.is_leader = True
        self.team_membership.save()

        request = make_mock_object(user=self.competitor, method='DELETE')
        self.assertTrue(self.permission.has_object_permission(request=request, view=None, obj=self.team_membership))

    def test_leader_can_post(self):
        self.team_membership.is_leader = True
        self.team_membership.save()
        data = {'team': self.team}

        request = make_mock_object(user=self.competitor, method='POST', data=data)
        self.assertTrue(self.permission.has_permission(request=request, view=None))
