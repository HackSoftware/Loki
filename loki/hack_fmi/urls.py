from django.conf.urls import url
from .views import SkillListView, TeamListView, CompetitorListView, register, Login

urlpatterns = [
    url(r'^api/skills/$', SkillListView.as_view(), name='skills'),
    url(r'^api/register/$', register, name='register'),
    url(r'^api/login/', Login.as_view(), name='login'),
    url(r'^api/competitors/$', CompetitorListView.as_view(), name='competitors'),
    url(r'^api/teams/$', TeamListView.as_view(), name='teams')
]
