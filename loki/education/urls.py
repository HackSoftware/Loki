from django.conf.urls import url
from education.views import (set_check_in, get_lectures, get_check_ins, StudentNoteAPI,
                             get_courses, OnBoardStudent, student_update, get_students_for_course,
                             drop_student, working_at, get_cities, get_companies, TasksAPI,
                             SolutionsAPI, CourseAssignmentAPI, certificate)

urlpatterns = [
    url(r'^api/set-check-in/$', set_check_in, name='set_check_in'),
    url(r'^api/get-lectures/$', get_lectures, name='get_lectures'),
    url(r'^api/get-check-ins/$', get_check_ins, name='get_check_ins'),
    url(r'^api/get-courses/$', get_courses, name='get_courses'),
    url(r'^api/student-update/$', student_update, name='student_update'),
    url(r'^api/onboard-student/$', OnBoardStudent.as_view(), name='onboard_student'),
    url(r'^api/get-students-for-course/$', get_students_for_course, name='get_students_for_course'),
# url(r'^api/get-cas-for-course/$', get_cas_for_course, name='get_ca_for_course'),
    url(r'^api/CourseAssignment/$', CourseAssignmentAPI.as_view(), name='course_assignment'),
    url(r'^api/note/$', StudentNoteAPI.as_view(), name='note'),
    url(r'^api/drop-student/$', drop_student, name='drop_student'),
    url(r'^api/working_at/$', working_at, name='working_at'),
    url(r'^api/get-cities/$', get_cities, name='get_cities'),
    url(r'^api/get-companies/$', get_companies, name='get_companies'),
    url(r'^api/task/$', TasksAPI.as_view(), name='task'),
    url(r'^api/solution/$', SolutionsAPI.as_view(), name='solution'),
    url(r'^api/solution/(?P<pk>[0-9]+)/$', SolutionsAPI.as_view(),  name='solution_edit'),
    url(r'^certificate/(?P<pk>[0-9]+)/$', certificate, name='certificate'),
]
