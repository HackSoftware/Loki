from django.db.models.signals import post_save
from django.dispatch import receiver

from loki.education.models import CourseAssignment


@receiver(post_save, sender=CourseAssignment)
def create_course_assignment(sender, instance, **kwargs):
    if instance.user:
        if instance.course:
            print("in if")
