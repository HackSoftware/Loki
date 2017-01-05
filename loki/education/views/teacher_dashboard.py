from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django.core.urlresolvers import reverse
from loki.education.models import (Course, Task, Solution, Student,
                                   CourseAssignment, StudentNote)
from ..mixins import (DashboardPermissionMixin,
                      CannotSeeOthersCoursesDashboardsMixin,
                      CanSeeCourseInfoOnlyTeacher)
from ..helper import task_solutions, latest_solution_statuses


class StudentListView(CanSeeCourseInfoOnlyTeacher,
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


class TaskListView(CanSeeCourseInfoOnlyTeacher,
                   DashboardPermissionMixin,
                   ListView):
    model = Task
    template_name = 'education/teacher_task_list.html'

    def get_queryset(self):
        course_id = self.kwargs.get("course")
        return Task.objects.filter(course=course_id)


class CourseDetailView(CanSeeCourseInfoOnlyTeacher,
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


class StudentTaskListView(CanSeeCourseInfoOnlyTeacher,
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


class StudentSolutionListView(CanSeeCourseInfoOnlyTeacher,
                              DashboardPermissionMixin,
                              ListView):

    model = Solution

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs.get("task"))
        student = Student.objects.get(id=self.kwargs.get("student"))
        return Solution.objects.filter(student=student, task=task).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.kwargs.get('course'))
        context['student'] = Student.objects.get(id=self.kwargs.get('student'))
        return context


class StudentNoteCreateView(CanSeeCourseInfoOnlyTeacher,
                            DashboardPermissionMixin,
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
