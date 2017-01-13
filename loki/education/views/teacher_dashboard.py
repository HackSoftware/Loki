from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django.core.urlresolvers import reverse
from loki.education.models import (Course, Task, Solution, Student,
                                   CourseAssignment, StudentNote)
from loki.education.mixins import (DashboardPermissionMixin,
                                   CannotSeeOthersCoursesDashboardsMixin,
                                   IsTeacherMixin)
from loki.education.helper import task_solutions, latest_solution_statuses
from loki.education.helper import get_dates_for_weeks, percentage_presence
from loki.education.models import CheckIn

class StudentListView(DashboardPermissionMixin,
                      IsTeacherMixin,
                      CannotSeeOthersCoursesDashboardsMixin,
                      ListView):
    """
        All students which have CourseAssignments
    """
    model = CourseAssignment

    def get_queryset(self):
        course_id = self.kwargs.get("course")
        return CourseAssignment.objects.filter(course__id=course_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.kwargs.get("course"))
        return context

class StudentDetailView(DashboardPermissionMixin,
                        IsTeacherMixin,
                        CannotSeeOthersCoursesDashboardsMixin,
                        DetailView):

    model = CourseAssignment
    pk_url_kwarg = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs.get("course"))
        tasks = Task.objects.filter(course=course, gradable=True)
        url_tasks = Task.objects.filter(course=course, gradable=False)

        student = Student.objects.get(id=self.object.user.id)
        context['passed_solutions'] = Solution.objects.filter(student=student, task__in=tasks, status=2).count()
        context['failed_solutions'] = Solution.objects.filter(student=student, task__in=tasks, status=3).count()
        context['url_solutions'] = Solution.objects.filter(student=student, task__in=url_tasks).count()
        context['count_solutions'] = context['passed_solutions'] + context['failed_solutions'] + context['url_solutions']

        course_presence = {}
        if course.lecture_set.exists():
            course_presence['weeks'] = list(get_dates_for_weeks(course).keys())
            course_presence['dates_for_weeks'] = get_dates_for_weeks(course)
            course_presence['user_dates'] = CheckIn.objects.get_user_dates(student, course)

            user_dates = course_presence['user_dates']
            course_presence['percentage_presence'] = percentage_presence(user_dates, course)

        context['course_presence'] = course_presence

        return context



class TaskListView(DashboardPermissionMixin,
                   IsTeacherMixin,
                   ListView):
    model = Task
    template_name = 'education/teacher_task_list.html'

    def get_queryset(self):
        course_id = self.kwargs.get("course")
        return Task.objects.filter(course=course_id)


class CourseDetailView(DashboardPermissionMixin,
                       IsTeacherMixin,
                       CannotSeeOthersCoursesDashboardsMixin,
                       DetailView):
    model = Course
    pk_url_kwarg = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_solutions'] = Solution.objects.filter(task__in=self.object.task_set.all()).count()

        gradable_tasks = Task.objects.get_tasks_for(course=self.object, gradable=True)
        context['gradable_tasks'] = gradable_tasks.count()
        context['passed_solutions'] = Solution.objects.filter(task__in=gradable_tasks, status=2).count()
        context['failed_solutions'] = Solution.objects.filter(task__in=gradable_tasks, status=3).count()

        not_gradable_tasks = Task.objects.get_tasks_for(course=self.object)
        context['not_gradable_tasks'] = not_gradable_tasks.count()
        context['url_solutions'] = Solution.objects.filter(task__in=not_gradable_tasks).count()

        return context


class StudentTaskListView(DashboardPermissionMixin,
                          IsTeacherMixin,
                          CannotSeeOthersCoursesDashboardsMixin,
                          ListView):

    model = Task

    def get_queryset(self):
        course_id = self.kwargs.get('course')
        return Task.objects.filter(course=course_id).order_by('-week')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.kwargs.get('course')
        context['course'] = Course.objects.get(id=course)
        context['student'] = Student.objects.get(id=self.kwargs.get('student'))
        solutions = Solution.objects.filter(student=self.kwargs.get('student')).filter(
                                            task__course__in=[course])
        context['tasksolution'] = task_solutions(solutions)
        tasks = Task.objects.filter(course=course)
        context['latest_solutions'] = latest_solution_statuses(self.kwargs.get('student'),
                                                               tasks)
        return context


class StudentSolutionListView(DashboardPermissionMixin,
                              IsTeacherMixin,
                              CannotSeeOthersCoursesDashboardsMixin,
                              ListView):

    model = Solution

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs.get("task"))
        self.student = Student.objects.get(id=self.kwargs.get('student'))
        return Solution.objects.filter(student=self.student, task=task).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.kwargs.get('course'))
        context['student'] = self.student
        return context


class StudentNoteCreateView(DashboardPermissionMixin,
                            IsTeacherMixin,
                            CreateView):

    model = StudentNote
    fields = ['assignment', 'text']

    def get_success_url(self):
        return reverse('education:student-list',
                       kwargs={'course': self.kwargs.get('course')})

    def form_valid(self, form):
        author = self.request.user.get_teacher()
        note = form.save(commit=False)
        note.author = author
        return super().form_valid(form)
