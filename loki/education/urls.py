from django.conf.urls import url

from loki.education.views import old_api_views, dashboard


urlpatterns = [
    url(r'^api/set-check-in/$', old_api_views.set_check_in, name='set_check_in'),
    url(r'^api/get-lectures/$', old_api_views.GetLectures.as_view(), name='get_lectures'),
    url(r'^api/get-courses/$', old_api_views.get_courses, name='get_courses'),
    url(r'^api/onboard-student/$', old_api_views.OnBoardStudent.as_view(), name='onboard_student'),
    url(r'^api/course-assignment/$', old_api_views.CourseAssignmentAPI.as_view(), name='get_ca_for_course'),
    url(r'^api/note/$', old_api_views.StudentNoteAPI.as_view(), name='note'),
    url(r'^api/working_at/$', old_api_views.working_at, name='working_at'),
    url(r'^api/get-cities/$', old_api_views.get_cities, name='get_cities'),
    url(r'^api/get-companies/$', old_api_views.get_companies, name='get_companies'),
    url(r'^api/task/$', old_api_views.TasksAPI.as_view(), name='task'),
    url(r'^api/solution/$', old_api_views.SolutionsAPI.as_view(), name='solution'),
    url(r'^api/solution/(?P<pk>[0-9]+)/$', old_api_views.SolutionsAPI.as_view(),  name='solution_edit'),
    url(r'^api/solution-status/(?P<pk>[0-9]+)/$', old_api_views.SolutionStatusAPI.as_view(), name='solution_status'),
    url(r'^api/student-solutions/$', old_api_views.StudentSolutionsList.as_view(), name='student_solutions'),
    url(r'^certificate/(?P<pk>[0-9]+)/$', old_api_views.certificate_old, name='certificate_old'),
    url(r'^certificate/(?P<token>[\w|-]+)/$', old_api_views.certificate, name='certificate'),
    url(r'^dashboard/$', dashboard.CourseListView.as_view(), name='course_list'),
    url(r'^course/(?P<course>[0-9]+)/dashboard/$',
        dashboard.CourseDashboardView.as_view(), name='course_dashboard'),
    url(r'^course/(?P<course>[0-9]+)/task/(?P<task>[0-9]+)/solutions/$',
        dashboard.SolutionView.as_view(), name='solution_view'),
    url(r'^course/(?P<course>[0-9]+)/materials/$',
        dashboard.MaterialView.as_view(), name='material_view'),
    url(r'^course/(?P<course>[0-9]+)/students/$',
        dashboard.StudentCourseView.as_view(), name='students_view'),
    url(r'^course/(?P<course>[0-9]+)/teacher-task-dashboard/$',
        dashboard.TeacherTaskView.as_view(), name='teacher_task_dashboard')
]
