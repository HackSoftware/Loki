from django.conf.urls import url

from loki.education.views import old_api_views, student_dashboard


urlpatterns = [
    url(r'^api/set-check-in/$', old_api_views.set_check_in, name='set_check_in'),
    url(r'^api/get-lectures/$', old_api_views.GetLectures.as_view(), name='get_lectures'),
    url(r'^api/get-check-ins/$', old_api_views.get_check_ins, name='get_check_ins'),
    url(r'^api/get-courses/$', old_api_views.get_courses, name='get_courses'),
    url(r'^api/student-update/$', old_api_views.student_update, name='student_update'),
    url(r'^api/onboard-student/$', old_api_views.OnBoardStudent.as_view(), name='onboard_student'),
    url(r'^api/get-students-for-course/$', old_api_views.get_students_for_course, name='get_students_for_course'),
    url(r'^api/course-assignment/$', old_api_views.CourseAssignmentAPI.as_view(), name='get_ca_for_course'),
    url(r'^api/note/$', old_api_views.StudentNoteAPI.as_view(), name='note'),
    url(r'^api/drop-student/$', old_api_views.drop_student, name='drop_student'),
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
    url(r'^dashboard/$', student_dashboard.CourseListView.as_view(), name='course_list'),
    url(r'^course/(?P<course>[0-9]+)/dashboard/$',
        student_dashboard.CourseDashboardView.as_view(), name='course_dashboard'),
    url(r'^course/(?P<course>[0-9]+)/task/(?P<task>[0-9]+)/solutions/$',
        student_dashboard.SolutionView.as_view(), name='solution_view'),
    url(r'^course/(?P<course>[0-9]+)/materials/$',
        student_dashboard.MaterialView.as_view(), name='material_view')
]
