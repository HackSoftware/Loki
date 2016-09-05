from django import template
from loki.website.models import CourseDescription

register = template.Library()


@register.inclusion_tag('apply_active_courses.html')
def get_apply_active_courses():
    courses = [cd for cd in CourseDescription.objects.all()
               if getattr(cd, 'applicationinfo', None) is not None]
    apply_courses = [cd for cd in courses if cd.applicationinfo.apply_is_active()]
    return {'apply_active_courses': apply_courses}
