import csv

from django.utils import timezone
from django.core.management.base import BaseCommand
from loki.education.models import Course, CourseAssignment, Student, WorkingAt


class Command(BaseCommand):
    help = "Create CSV file with all information about working ats"

    def handle(self, **options):
        # Without paid courses - AngularJS, NodeJS, Angular 2 and active courses
        angular_js = Course.objects.get(id=4)
        node_js = Course.objects.get(id=6)
        angular_2 = Course.objects.get(id=26)
        courses = Course.objects.exclude(id__in=[angular_js.id, node_js.id, angular_2.id]).filter(end_time__lte=timezone.now())

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
