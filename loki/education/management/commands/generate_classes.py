from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.core.management.base import BaseCommand
from education.models import Lecture, Course


class Command(BaseCommand):
    args = '<course_name number_of_weeks start_date:dd-mm-yyyy or "@" mon tues weds thurs fri sat sun'
    help = 'Generates entries in classes table'

    def get_day_number(self, day):
        if day == 'mon':
            return 1
        elif day == 'tues':
            return 2
        elif day == 'weds':
            return 3
        elif day == 'thurs':
            return 4
        elif day == 'fri':
            return 5
        elif day == 'sat':
            return 6
        elif day == 'sun':
            return 7
        else:
            raise ValueError(
                'Invalid format for date. Valid formats are:'
                'mon tues weds thurs fri sat sun'
            )

    def handle(self, *args, **options):
        course_id = int(args[0])
        weeks = int(args[1])
        course = get_object_or_404(Course, id=course_id)

        if args[2] == '@':
            date = course.start_time
        else:
            date = datetime.strptime(args[2], '%Y-%m-%d')
        days = list(map(self.get_day_number, args[3::]))

        start_date = date
        end_date = date + timedelta(days=weeks*7)

        while start_date <= end_date:
            if start_date.isoweekday() in days:
                Lecture.objects.create(
                    course=course,
                    date=start_date.strftime("%Y-%m-%d")
                )
            start_date += timedelta(days=1)
