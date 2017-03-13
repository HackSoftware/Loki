from django.core.management.base import BaseCommand
from django.utils import timezone
from loki.education.models import Course, Certificate


class Command(BaseCommand):

    def handle(self, *args, **options):
        courses = Course.objects.filter(generate_certificates_until__gt=timezone.now())
        for course in courses:
            for assignment in course.courseassignment_set.filter(is_attending=True):
                # print("Generate certificate for {}".format(assignment))
                cert, is_new = Certificate.objects.get_or_create(assignment=assignment)
