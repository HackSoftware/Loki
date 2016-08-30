from django import template
from loki.website.models import CourseDescription

register = template.Library()


@register.inclusion_tag('website/active_courses.html')
def get_active_courses():
    active_courses = CourseDescription.objects.all().order_by('-course__start_time')
    return {'active_courses': active_courses}
