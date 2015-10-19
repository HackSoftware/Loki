from django import template
from website.models import CourseDescription

register = template.Library()


@register.inclusion_tag('website/active_courses.html')
def get_active_courses():
    active_courses = CourseDescription.objects.all()
    return {'active_courses': active_courses}
