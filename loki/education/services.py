from django.core.exceptions import ValidationError

from loki.base_app.models import BaseUser

from loki.education.models import CheckIn, Teacher, CourseAssignment, Student
from loki.education.helper import get_dates_for_weeks, percentage_presence


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
