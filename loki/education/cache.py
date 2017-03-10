from django.core.cache import cache

#  cache.set("key", "value", timeout=None)


def get_student_cache_key_for_course(course_assignment):
    return "course_assignment_{}_progress_cache_key_for_traininig".format(course_assignment.id)
