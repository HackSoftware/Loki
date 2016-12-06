from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from loki.education.models import (Course, Task, Solution, Material, CheckIn,
                                   Student)
from ..mixins import (DashboardPermissionMixin,
                      CannotSeeOthersCoursesDashboardsMixin,
                      CannotSeeCourseTaskListMixin,
                      CanSeeCourseInfoOnlyTeacher)
from ..helper import (get_dates_for_weeks, task_solutions,
                      latest_solution_statuses, percentage_presence)


class CourseListView(DashboardPermissionMixin, ListView):

    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.get_student():
            user = self.request.user.student
        else:
            user = self.request.user.teacher

        course_presence = {}
        for course in self.get_queryset():
            if not course.lecture_set.exists():
                continue
            course_presence[course] = {}
            course_presence[course]['weeks'] = list(get_dates_for_weeks(course).keys())
            course_presence[course]['dates_for_weeks'] = get_dates_for_weeks(course)
            course_presence[course]['user_dates'] = CheckIn.objects.get_user_dates(user, course)

            user_dates = course_presence[course]['user_dates']
            course_presence[course]['percentage_presence'] = percentage_presence(user_dates, course)

        context['course_presence'] = course_presence

        return context

    def get_queryset(self):
        if self.request.user.get_teacher():
            return self.request.user.teacher.teached_courses.all()
        if self.request.user.get_student():
            return Course.objects.filter(courseassignment__user=self.request.user).order_by('-end_time')


class TaskDashboardView(DashboardPermissionMixin,
                        CannotSeeOthersCoursesDashboardsMixin,
                        CannotSeeCourseTaskListMixin,
                        ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.kwargs.get('course')
        solutions = Solution.objects.filter(student=self.request.user.student).filter(
                                            task__course__in=[course])
        context['tasksolution'] = task_solutions(solutions)
        tasks = Task.objects.filter(course=self.course)
        context['latest_solutions'] = latest_solution_statuses(self.request.user.student,
                                                               tasks)
        return context

    def get_queryset(self):
        return Task.objects.filter(course=self.course).order_by('-week')

    def post(self, request, *args, **kwargs):
        url = self.request.POST['url']
        task_id = self.request.POST['task']
        task = Task.objects.filter(id=task_id).first()
        Solution.objects.create(student=self.request.user.student,
                                url=url,
                                task=task)

        return super().get(request, *args, **kwargs)


class SolutionView(DashboardPermissionMixin,
                   CannotSeeOthersCoursesDashboardsMixin,
                   ListView):
    model = Solution

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs.get("task"))
        return Solution.objects.filter(student=self.request.user, task=task).order_by("-created_at")


class MaterialView(DashboardPermissionMixin,
                   CannotSeeOthersCoursesDashboardsMixin,
                   ListView):
    model = Material

    def get_queryset(self):
        return Material.objects.filter(course=self.course).order_by("-week")


class StudentCourseView(CanSeeCourseInfoOnlyTeacher,
                        CannotSeeOthersCoursesDashboardsMixin,
                        ListView):
    model = Student

    def get_queryset(self):
        course_id = self.kwargs.get("course")
        return Student.objects.filter(courses__id__exact=course_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.kwargs.get("course"))
        return context


class TeacherTaskView(CanSeeCourseInfoOnlyTeacher,
                      DashboardPermissionMixin,
                      ListView):
    """
    Teacher View for creating, editing and deleting tasks
    """
    model = Task
    template_name = 'education/teacher_task_list.html'

    def get_queryset(self):
        course_id = self.kwargs.get("course")
        return Task.objects.filter(course=course_id)


class CourseDashboardView(CanSeeCourseInfoOnlyTeacher,
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


class CourseStudentTaskView(CanSeeCourseInfoOnlyTeacher,
                            DashboardPermissionMixin,
                            ListView):

    model = Task
    template_name = 'education/student_tasks_list.html'

    def get_queryset(self):
        course_id = self.kwargs.get('course')
        return Task.objects.filter(course=course_id).order_by('-week')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.kwargs.get('course')
        context['course'] = Course.objects.get(id=course)
        solutions = Solution.objects.filter(student=self.kwargs.get('student')).filter(
                                            task__course__in=[course])
        context['tasksolution'] = task_solutions(solutions)
        tasks = Task.objects.filter(course=course)
        context['latest_solutions'] = latest_solution_statuses(self.kwargs.get('student'),
                                                               tasks)
        return context
