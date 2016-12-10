from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from .views import (MeAPIView, SkillListAPIView, TeamAPI, InvitationViewSet,
                    MentorListView, SeasonView, PublicTeamView,
                    get_schedule, schedule_json, OnBoardCompetitorAPI, TeamMembershipAPI,
                    TeamMentorshipAPI, TestApi, MeSeasonAPIView, CompetitorListAPIView,
                    SeasonInfoAPI, JWTLogoutView, CustomRefreshJSONWebTokenAPIView)


from .auth import Login
# from .signals import send_invitation

from djoser import views

invitation_urls = InvitationViewSet.get_urls()

"""
  Every time a query is send, depending on the exact type of the query,
  a different method of the InvitationViewSet is called.
"""

router = routers.SimpleRouter()
router.register(r'api/teams', TeamAPI)


urlpatterns = [
    url(r'^api/jwt-login/$', obtain_jwt_token, name='api-login'),
    # check for JWT auth
    url(r'^api/jwt-test/$', TestApi.as_view(), name='test_api'),

    url(r'^api/jwt-refresh/$', CustomRefreshJSONWebTokenAPIView.as_view(), name='api-refresh'),

    url(r'^api/jwt-logout/$', JWTLogoutView.as_view(), name='api-logout'),


    url(r'^api/skills/$', SkillListAPIView.as_view(), name='skills'),

    url(r'^api/season/$', SeasonView.as_view(), name='season'),

    url(r'^api/public-teams/', PublicTeamView.as_view(), name='public_teams'),

    url(r'^api/mentors/$', MentorListView.as_view(), name='mentors'),

    url(r'^api/team-membership/(?P<pk>[0-9]+)/$', TeamMembershipAPI.as_view(), name='team_membership'),

    url(r'^api/team-mentorship/(?P<mentor_pk>[0-9]+)?', TeamMentorshipAPI.as_view(), name='team_mentorship'),

    url(r'^api/invitation/$', invitation_urls['invitation_list'], name='invitation-list'),
    url(r'^api/invitation/(?P<pk>[0-9]+)/$', invitation_urls['invitation_detail'], name='invitation-detail'),
    url(r'^api/invitation/(?P<pk>[0-9]+)/accept/$', invitation_urls['invitation_accept'], name='invitation-accept'),

    # Auth
    url(r'^api/login/', Login.as_view(), name='login'),
    url(r'^api/logout/$', views.LogoutView.as_view(), name='logout'),

    url(r'^api/me/$', MeAPIView.as_view(), name='me'),
    # TODO: change season_pk to get parameter
    url(r'^api/me/(?P<season_pk>[0-9]+)/$', MeSeasonAPIView.as_view(), name='me-season'),

    url(r'^api/schedule/', get_schedule, name="get_schedule"),
    url(r'^api/schedule-json/', schedule_json, name="schedule_json"),
    url(r'^api/onboard-competitor/$', OnBoardCompetitorAPI.as_view(), name='onboard_competitor'),
    url(r'^api/competitors/$', CompetitorListAPIView.as_view(), name='competitors'),
    url(r'^api/season-competitor-info/$', SeasonInfoAPI.as_view(), name='season_competitor_info'),
    url(r'^api/season-competitor-info/(?P<pk>[0-9]+)/$', SeasonInfoAPI.as_view(), name='season_competitor_info_detail'),
] + router.urls
