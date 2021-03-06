import csv

from django.utils import timezone
from django.core.management.base import BaseCommand
from loki.education.models import Course, CourseAssignment, Student, WorkingAt


class Command(BaseCommand):
    help = "Create CSV file with all information about working ats"

    def add_arguments(self, parser):
        parser.add_argument('paid_courses',
                            help='Provide ids of paid courses as string "1, 2, 3"')

    def handle(self, **options):
        # Without paid courses - AngularJS, NodeJS, Angular 2 and active courses
        courses = options['paid_courses'].split(',')
        courses = [int(course_id) for course_id in courses]
        courses = Course.objects.exclude(
                                id__in=courses).filter(
                                end_time__lte=timezone.now())

        student_ids = CourseAssignment.objects.filter(course__in=courses).values_list('user', flat=True).distinct()

        with open('working_ats.csv', 'w') as csvfile:
            fieldnames = ["Name", "email", "Courses", "Working Ats"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for s_id in student_ids:
                student = Student.objects.get(id=s_id)
                courses_ids = student.courseassignment_set.values_list('course', flat=True).all()
                courses = Course.objects.filter(id__in=courses_ids).order_by('-start_time')
                working_ats = WorkingAt.objects.filter(student=student).order_by('-start_date')
                working_ats = "" if not working_ats else working_ats

                row = {"Name": student,
                       "email": student.email,
                       "Courses": courses,
                       "Working Ats": working_ats}

                writer.writerow(row)
