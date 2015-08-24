from django.core.management.base import BaseCommand
from django.utils import timezone
from education.models import Course, OldCertificate


class Command(BaseCommand):
    def handle(self, *args, **options):
        courses = Course.object.find(generate_certificates_until__lt=timezone.now())
        for course in courses:
            for assignment in course.courseassignment_set.all():
                cert, is_new = OldCertificate.object.get_or_create(assignment=assignment)
