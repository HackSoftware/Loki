from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/set-check-in/$', views.set_check_in, name='set_check_in'),
    url(r'^api/get-lectures/$', views.GetLectures.as_view(), name='get_lectures'),
    url(r'^api/get-check-ins/$', views.get_check_ins, name='get_check_ins'),
    url(r'^api/get-courses/$', views.get_courses, name='get_courses'),
    url(r'^api/student-update/$', views.student_update, name='student_update'),
    url(r'^api/onboard-student/$', views.OnBoardStudent.as_view(), name='onboard_student'),
    url(r'^api/get-students-for-course/$', views.get_students_for_course, name='get_students_for_course'),
    url(r'^api/course-assignment/$', views.CourseAssignmentAPI.as_view(), name='get_ca_for_course'),
    url(r'^api/note/$', views.StudentNoteAPI.as_view(), name='note'),
    url(r'^api/drop-student/$', views.drop_student, name='drop_student'),
    url(r'^api/working_at/$', views.working_at, name='working_at'),
    url(r'^api/get-cities/$', views.get_cities, name='get_cities'),
    url(r'^api/get-companies/$', views.get_companies, name='get_companies'),
    url(r'^api/task/$', views.TasksAPI.as_view(), name='task'),
    url(r'^api/solution/$', views.SolutionsAPI.as_view(), name='solution'),
    url(r'^api/solution/(?P<pk>[0-9]+)/$', views.SolutionsAPI.as_view(),  name='solution_edit'),
    url(r'^api/solution-status/(?P<pk>[0-9]+)/$', views.SolutionStatusAPI.as_view(), name='solution_status'),
    url(r'^api/student-solutions/$', views.StudentSolutionsList.as_view(), name='student_solutions'),
    url(r'^certificate/(?P<pk>[0-9]+)/$', views.certificate_old, name='certificate_old'),
    url(r'^certificate/(?P<token>[\w|-]+)/$', views.certificate, name='certificate'),
]
