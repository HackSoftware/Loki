from django import template
from loki.education.helper import calculate_student_progress_for_course_in_percents

register = template.Library()


@register.simple_tag
def get_student_progress_for_course(course_assignment):
    return calculate_student_progress_for_course_in_percents(course_assignment)
