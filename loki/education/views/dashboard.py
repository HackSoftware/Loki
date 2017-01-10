from django.views.generic.list import ListView
from django.views.generic import TemplateView
from loki.education.models import Course, Material, CheckIn
from loki.education.mixins import (DashboardPermissionMixin,
                                   CannotSeeOthersCoursesDashboardsMixin)
from loki.education.helper import get_dates_for_weeks, percentage_presence


class CourseListView(DashboardPermissionMixin,
                     TemplateView):

    template_name = 'education/course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.get_teacher():
            context['t_courses'] = self.request.user.teacher.teached_courses.all()
        else:
            context['t_courses'] = None
        if self.request.user.get_student():
            context['st_courses'] = Course.objects.filter(
                courseassignment__user=self.request.user).order_by('-end_time')
        else:
            context['st_courses'] = None
        if self.request.user.get_student():
            st_user = self.request.user.student
        if self.request.user.get_teacher():
            t_user = self.request.user.teacher

        t_course_presence = {}
        if context['t_courses']:
            for course in context['t_courses']:
                if not course.lecture_set.exists():
                    continue
                t_course_presence[course] = {}
                t_course_presence[course]['weeks'] = list(get_dates_for_weeks(course).keys())
                t_course_presence[course]['dates_for_weeks'] = get_dates_for_weeks(course)
                t_course_presence[course]['user_dates'] = CheckIn.objects.get_user_dates(t_user, course)

                user_dates = t_course_presence[course]['user_dates']
                t_course_presence[course]['percentage_presence'] = percentage_presence(user_dates, course)

        context['t_course_presence'] = t_course_presence

        st_course_presence = {}
        if context['st_courses']:
            for course in context['st_courses']:
                if not course.lecture_set.exists():
                    continue
                st_course_presence[course] = {}
                st_course_presence[course]['weeks'] = list(get_dates_for_weeks(course).keys())
                st_course_presence[course]['dates_for_weeks'] = get_dates_for_weeks(course)
                st_course_presence[course]['user_dates'] = CheckIn.objects.get_user_dates(st_user, course)

                user_dates = st_course_presence[course]['user_dates']
                st_course_presence[course]['percentage_presence'] = percentage_presence(user_dates, course)

        context['st_course_presence'] = st_course_presence

        return context


class MaterialListView(DashboardPermissionMixin,
                       CannotSeeOthersCoursesDashboardsMixin,
                       ListView):
    model = Material

    def get_queryset(self):
        return Material.objects.filter(course=self.course).order_by("-week")
