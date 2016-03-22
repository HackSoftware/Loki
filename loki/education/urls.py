from django.conf.urls import url
from education.views import *

urlpatterns = [
    url(r'^api/set-check-in/$', set_check_in, name='set_check_in'),
    url(r'^api/get-lectures/$', get_lectures, name='get_lectures'),
    url(r'^api/get-check-ins/$', get_check_ins, name='get_check_ins'),
    url(r'^api/get-courses/$', get_courses, name='get_courses'),
    url(r'^api/student-update/$', student_update, name='student_update'),
    url(r'^api/onboard-student/$', OnBoardStudent.as_view(), name='onboard_student'),
    url(r'^api/get-students-for-course/$', get_students_for_course, name='get_students_for_course'),
    url(r'^api/course-assignment/$', CourseAssignmentAPI.as_view(), name='get_ca_for_course'),
    url(r'^api/note/$', StudentNoteAPI.as_view(), name='note'),
    url(r'^api/drop-student/$', drop_student, name='drop_student'),
    url(r'^api/working_at/$', working_at, name='working_at'),
    url(r'^api/get-cities/$', get_cities, name='get_cities'),
    url(r'^api/get-companies/$', get_companies, name='get_companies'),
    url(r'^api/task/$', TasksAPI.as_view(), name='task'),
    url(r'^api/solution/$', SolutionsAPI.as_view(), name='solution'),
    url(r'^api/solution/(?P<pk>[0-9]+)/$', SolutionsAPI.as_view(),  name='solution_edit'),
    url(r'^api/solution-status/(?P<pk>[0-9]+)/$', SolutionStatusAPI.as_view(), name='solution_status'),
    url(r'^api/student-solutions/$', StudentSolutionsList.as_view(), name='student_solutions'),
    url(r'^certificate/(?P<pk>[0-9]+)/$', certificate_old, name='certificate_old'),
    url(r'^certificate/(?P<token>[\w|-]+)/$', certificate, name='certificate'),
]
