from django.conf.urls import url
from .views import SkillListView, TeamListView, CompetitorListView, register, Login, register_team, me, CustomRegistrationView
from djoser.views import ActivationView, LogoutView, UserView

urlpatterns = [
    url(r'^api/skills/$', SkillListView.as_view(), name='skills'),
    url(r'^api/register/$', register, name='register'),
    url(r'^api/register_team/$', register_team, name='register_team'),
    url(r'^api/competitors/$', CompetitorListView.as_view(), name='competitors'),
    url(r'^api/teams/$', TeamListView.as_view(), name='teams'),

    url(r'^api/new-register/$', CustomRegistrationView.as_view()),
    url(r'^api/login/', Login.as_view(), name='login'),
    url(r'^api/logout/$', ActivationView.as_view(), name='activate'),
    url(r'^api/activate/$', LogoutView.as_view(), name='activate'),
    url(r'^api/me/$', UserView.as_view(), name='me'),

]
