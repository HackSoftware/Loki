from math import ceil
from datetime import datetime

from django.core.management import BaseCommand

from loki.education.models import Course, CheckIn, Lecture


class Command(BaseCommand):
    args = '<start_date> <end_date> in format year-month-day'
    help = 'Checks presence percentage for each student in current courses or in courses in set period'

    def handle(self, *args, **options):
        if len(args) == 0:
            courses = Course.objects.filter(
                end_time__gte=datetime.now(),
                start_time__lte=datetime.now()
            )
            for course in courses:
                start_time = course.start_time
                end_time = course.end_time
                cas = course.courseassignment_set.all()
                lectures = Lecture.objects.filter(course=course, date__lte=datetime.now()).all()
                lecture_dates = [lecture.date for lecture in lectures]
                for ca in cas:
                    student_id = ca.user.id
                    check_ins = CheckIn.objects.filter(student_id=student_id,
                                                       date__gte=start_time,
                                                       date__lte=end_time,
                                                       )
                    times_been = 0
                    for check_in in check_ins:
                        if check_in.date in lecture_dates:
                            times_been += 1
                    student_presence = ceil((times_been / len(lecture_dates)) * 100)
                    ca.student_presence = student_presence
                    ca.save()