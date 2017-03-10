from django.core.exceptions import ValidationError

from loki.base_app.models import BaseUser

from loki.education.models import CheckIn, Teacher, CourseAssignment, Student, Solution
from loki.education.helper import get_dates_for_weeks, percentage_presence
from loki.education.decorators import cache_progress_result
from loki.education.cache import get_student_cache_key_for_course_data


def get_course_presence(*, course, user):
    course_presence = {}
    if course.lecture_set.exists():
        course_presence['weeks'] = list(get_dates_for_weeks(course).keys())
        course_presence['dates_for_weeks'] = get_dates_for_weeks(course)
        course_presence['user_dates'] = CheckIn.objects.get_user_dates(user, course)

        user_dates = course_presence['user_dates']
        course_presence['percentage_presence'] = percentage_presence(user_dates, course)

    return course_presence


def add_student_to_course(*, user, course, group_time=CourseAssignment.LATE):
    teacher = user.get_teacher()
    if teacher and course in teacher.teached_courses.all():
        raise ValidationError("{} is teacher for this course".format(teacher))

    student = user.get_student()
    if student and student.id in course.courseassignment_set.values_list('user', flat=True):
        raise ValidationError("{} has already courseassignment for this course".format(student))

    if not student:
        BaseUser.objects.promote_to_student(user)

    student = Student.objects.filter(email=user.email).first()
    CourseAssignment.objects.create(user=student,
                                    course=course,
                                    group_time=group_time)

    return student


def add_teacher_to_course(*, user, course):
    student = user.get_student()
    if student and student.id in course.courseassignment_set.values_list('user', flat=True):
        raise ValidationError("{} has courseassingment for this course".format(student))

    teacher = user.get_teacher()
    if teacher and course in teacher.teached_courses.all():
        raise ValidationError("{} is already teacher for this course".format(teacher))

    if not teacher:
        teacher = BaseUser.objects.promote_to_teacher(user)
        teacher.teached_courses = [course]
        teacher.save()

    teacher = Teacher.objects.filter(email=user.email).first()
    teacher.teached_courses.add(course)
    teacher.save()

    return teacher


@cache_progress_result(key_function=get_student_cache_key_for_course_data)
def get_student_data_for_course(course_assignment):
    course_data = {"gradable_tasks": [],
                   "url_tasks": []}
    course = course_assignment.course
    student = course_assignment.user

    gradable_tasks = course.task_set.filter(gradable=True).all()
    url_tasks = course.task_set.filter(gradable=False).all()

    all_tasks = gradable_tasks.count() + url_tasks.count()
    total = 0

    for gradable_task in gradable_tasks:
        status = "Not sent"

        passed_solutions = gradable_task.solution_set.filter(status=Solution.OK, student=student)
        failed_solutions = gradable_task.solution_set.filter(status=Solution.NOT_OK, student=student)

        if passed_solutions.exists():
            status = "PASS"
            total += 1

        if failed_solutions.exists() and not passed_solutions.exists():
            status = "FAIL"

        course_data["gradable_tasks"].append({"name": gradable_task.name,
                                              "description": gradable_task.description,
                                              "week": gradable_task.week,
                                              "solution_status": status})

    for task in url_tasks:
        solution = False

        if task.solution_set.filter(student=student).exists():
            solution = task.solution_set.last().url
            total += 1

        course_data["url_tasks"].append({"name": task.name,
                                         "description": task.description,
                                         "week": task.week,
                                         "solution": solution})

    percent_awesome = round((total/all_tasks) * 100, 2)
    course_data['percent_awesome'] = percent_awesome
    return course_data
