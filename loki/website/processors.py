from loki.website.models import CourseDescription


def active_courses(request):
    active_courses = CourseDescription.objects.all().order_by('-course__start_time')
    return {'active_courses': active_courses}
