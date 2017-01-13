from loki.education.models import CheckIn
from loki.education.helper import get_dates_for_weeks, percentage_presence


def get_course_presence(course, student):
    course_presence = {}
    if course.lecture_set.exists():
        course_presence['weeks'] = list(get_dates_for_weeks(course).keys())
        course_presence['dates_for_weeks'] = get_dates_for_weeks(course)
        course_presence['user_dates'] = CheckIn.objects.get_user_dates(student, course)

        user_dates = course_presence['user_dates']
        course_presence['percentage_presence'] = percentage_presence(user_dates, course)

    return course_presence
