from django.conf.urls import url

from .views import (SkillListView, TeamAPI, leave_team, InvitationView,
                    MentorListView, SeasonListView, AssignMentor, PublicTeamView,
                    get_schedule, schedule_json, OnBoardCompetitor)
from .auth import Login, me


urlpatterns = [
    url(r'^api/skills/$', SkillListView.as_view(), name='skills'),

    url(r'^api/teams/(?P<pk>[0-9]+)?', TeamAPI.as_view(), name='teams'),

    url(r'^api/public-teams/', PublicTeamView.as_view(), name='public_teams'),

    url(r'^api/mentors/$', MentorListView.as_view(), name='mentors'),

    url(r'^api/leave_team/$', leave_team, name='leave_team'),

    url(r'^api/invitation/$', InvitationView.as_view(), name='invitation'),
    # Auth
    url(r'^api/login/', Login.as_view(), name='login'),
    # url(r'^api/logout/$', LogoutView.as_view(), name='logout'),

    url(r'^api/me/$', me, name='me'),
    url(r'^api/season/$', SeasonListView.as_view(), name='season'),
    url(r'^api/assign_mentor/$', AssignMentor.as_view(), name='assign_mentor'),

    url(r'^api/schedule/', get_schedule, name="get_schedule"),
    url(r'^api/schedule_json/', schedule_json, name="schedule_json"),
    url(r'^onboard-competitor/$', OnBoardCompetitor.as_view(), name='onboard_competitor'),
]
