from loki.website.models import CourseDescription


def apply_active_courses(request):
    courses = [cd for cd in CourseDescription.objects.all()
               if getattr(cd, 'applicationinfo', None) is not None]
    apply_courses = [cd for cd in courses if cd.applicationinfo.apply_is_active()]
    return {'apply_active_courses': apply_courses}
