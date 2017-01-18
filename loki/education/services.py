from loki.base_app.models import BaseUser

from loki.education.models import CheckIn, Teacher, CourseAssignment, Student
from loki.education.helper import get_dates_for_weeks, percentage_presence
from loki.education.exceptions import CannotBeStudentForSameCourse, CannotBeTeacherForSameCourse


def get_course_presence(*, course, user):
    course_presence = {}
    if course.lecture_set.exists():
        course_presence['weeks'] = list(get_dates_for_weeks(course).keys())
        course_presence['dates_for_weeks'] = get_dates_for_weeks(course)
        course_presence['user_dates'] = CheckIn.objects.get_user_dates(user, course)

        user_dates = course_presence['user_dates']
        course_presence['percentage_presence'] = percentage_presence(user_dates, course)

    return course_presence


def check_user_is_teacher_for_course(teacher, course):
    if course in teacher.teached_courses.all():
        raise CannotBeStudentForSameCourse


def check_user_is_student_for_course(student, course):
    if student.id in course.courseassignment_set.values_list('user', flat=True):
        raise CannotBeTeacherForSameCourse


def add_student_to_course(*, user, course, group_time=CourseAssignment.LATE):
    if user.get_teacher():
        check_user_is_teacher_for_course(teacher=user.get_teacher(), course=course)

    if not user.get_student():
        BaseUser.objects.promote_to_student(user)

    student = Student.objects.filter(email=user.email).first()
    CourseAssignment.objects.create(user=student,
                                    course=course,
                                    group_time=group_time)


def add_teacher_to_course(*, user, course):
    if user.get_student():
        check_user_is_student_for_course(student=user.get_student(), course=course)

    if not user.get_teacher():
        teacher = BaseUser.objects.promote_to_teacher(user)
        teacher.teached_courses = [course]
        teacher.save()

    teacher = Teacher.objects.filter(email=user.email).first()
    teacher.teached_courses.add(course)
    teacher.save()
