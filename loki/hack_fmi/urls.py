from django.conf.urls import url

from djoser.views import ActivationView, LogoutView, PasswordResetConfirmView

from .views import SkillListView, TeamAPI, leave_team, InvitationView, MentorListView, SeasonListView, AssignMentor
from .auth import Login, RegistrationView, me, PasswordResetView


urlpatterns = [
    url(r'^api/skills/$', SkillListView.as_view(), name='skills'),

    url(r'^api/teams/(?P<pk>[0-9]+)?', TeamAPI.as_view(), name='teams'),

    url(r'^api/mentors/$', MentorListView.as_view(), name='mentors'),

    url(r'^api/leave_team/$', leave_team, name='leave_team'),

    url(r'^api/invitation/$', InvitationView.as_view(), name='invitation'),
    # Auth
    url(r'^api/register/$', RegistrationView.as_view(), name='register'),
    url(r'^api/login/', Login.as_view(), name='login'),
    # url(r'^api/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/activate/$', ActivationView.as_view(), name='activate'),
    url(r'^api/password_reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^api/password_reset_confirm/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),


    url(r'^api/me/$', me, name='me'),
    url(r'^api/season/$', SeasonListView.as_view(), name='season'),
    url(r'^api/assign_mentor/$', AssignMentor.as_view(), name='assign_mentor'),
]
