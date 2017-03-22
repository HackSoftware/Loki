from django.conf.urls import url

from loki.education.views import old_api_views, dashboard, student_dashboard, teacher_dashboard


urlpatterns = [
    url(r'^api/set-check-in/$', old_api_views.set_check_in, name='set_check_in'),
    url(r'^api/solution/$', old_api_views.SolutionsAPI.as_view(), name='solution'),
    url(r'^api/solution/(?P<pk>[0-9]+)/$', old_api_views.SolutionsAPI.as_view(),  name='solution_edit'),
    url(r'^api/solution-status/(?P<pk>[0-9]+)/$', old_api_views.SolutionStatusAPI.as_view(), name='solution_status'),
    url(r'^certificate/(?P<token>[0-9a-f-]+)/$',
        student_dashboard.CertificateDetailView.as_view(), name="certificate-detail"),
    # Common views for Teacher Dashboard and Student Dashboard
    url(r'^dashboard/$', dashboard.CourseListView.as_view(), name='course-list'),
    url(r'^course/(?P<course>[0-9]+)/materials/$',
        dashboard.MaterialListView.as_view(), name='material-list'),
    # Student views
    url(r'^course/(?P<course>[0-9]+)/dashboard/$',
        student_dashboard.TaskListView.as_view(), name='task-list'),
    url(r'^course/(?P<course>[0-9]+)/task/(?P<task>[0-9]+)/solutions/$',
        student_dashboard.SolutionListView.as_view(), name='solution-list'),
    # Teacher views
    url(r'^course/(?P<course>[0-9]+)/students/$',
        teacher_dashboard.StudentListView.as_view(), name='student-list'),
    url(r'^course/(?P<course>[0-9]+)/students/(?P<ca>[0-9]+)$',
        teacher_dashboard.StudentDetailView.as_view(), name='student-detail'),
    url(r'^teacher/course/(?P<course>[0-9]+)/$',
        teacher_dashboard.CourseDetailView.as_view(), name='course-detail'),
    url(r'^course/(?P<course>[0-9]+)/teacher-task-dashboard/$',
        teacher_dashboard.TaskListView.as_view(), name='teacher-task-list'),
    url(r'^course/(?P<course>[0-9]+)/(?P<student>[0-9]+)/tasks/$',
        teacher_dashboard.StudentTaskListView.as_view(), name='student-task-list'),
    url(r'^course/(?P<course>[0-9]+)/(?P<student>[0-9]+)/tasks/(?P<task>[0-9]+)/$',
        teacher_dashboard.StudentSolutionListView.as_view(), name='student-solution-list'),
    url(r'^student-note-create/(?P<course>[0-9]+)/$',
        teacher_dashboard.StudentNoteCreateView.as_view(), name='student-note-create'),
    url(r'^student-note-update/(?P<course>[0-9]+)/(?P<studentnote>[0-9]+)$',
        teacher_dashboard.StudentNoteUpdateView.as_view(), name='student-note-update'),
    url(r'^course/(?P<course>[0-9]+)/drop-student/(?P<ca>[0-9]+)/$',
        teacher_dashboard.DropStudentView.as_view(), name='drop-student')
]
