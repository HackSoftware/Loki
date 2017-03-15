from django.db.models.signals import post_save
from django.dispatch import receiver

from loki.education.models import Solution
from loki.education.cache import delete_cache_for_courseassingment


@receiver(post_save, sender=Solution)
def delete_cache(sender, instance, created, **kwargs):

    course = instance.task.course
    course_assignment = instance.student.courseassignment_set.filter(course=course).first()
    delete_cache_for_courseassingment(course_assignment)
