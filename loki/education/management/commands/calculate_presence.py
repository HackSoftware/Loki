from django.core.management.base import BaseCommand
from loki.education.models import Course, CheckIn


class Command(BaseCommand):
    help = "Calculate presence"

    def handle(self, **options):

        active_courses = Course.objects.get_active_courses()

        for course in active_courses:
            course_assignments = course.courseassignment_set.all()
            lectures = course.lecture_set.values_list('date', flat=True)

            if lectures:
                for ca in course_assignments:
                    student = ca.user
                    all_student_checkins = CheckIn.objects.get_user_dates(user=student, course=course)
                    student_dates = [ci for ci in all_student_checkins if ci in lectures]

                    percentage_presence = int((len(student_dates) / len(lectures)) * 100)
                    ca.student_presence = percentage_presence
                    ca.save()
