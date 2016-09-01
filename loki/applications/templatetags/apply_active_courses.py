from django import template
from loki.applications.models import ApplicationInfo
from loki.education.models import Course

register = template.Library()

@register.inclusion_tag('apply_active_courses.html')
def get_apply_active_courses():
    courses = [x for x in Course.objects.all() \
                    if getattr(x, 'applicationinfo', None) is not None and \
                       getattr(x, 'coursedescription', None) is not None]
    apply_courses = [x for x in courses if x.applicationinfo.apply_is_active()]
    return {'apply_active_courses': apply_courses}
