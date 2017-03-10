from django.core.cache import cache

#  cache.set("key", "value", timeout=None)


def get_student_cache_key_for_course_data(course_assignment):
    return "course_assignment_{}_data_for_course".format(course_assignment.id)


def delete_cache_for_courseassingment(course_assignment):
    cache_key_for_course = get_student_cache_key_for_course_data(course_assignment)
    cache.delete(cache_key_for_course_assingment)
    cache.delete(cache_key_for_course)
