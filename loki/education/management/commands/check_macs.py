from django.core.management.base import BaseCommand
from education.models import CheckIn, Student


class Command(BaseCommand):
    help = 'distributes the teams in rooms'

    def handle(self, *args, **options):
        all_students = Student.objects.all()
        all_checkins = CheckIn.objects.all()

        mac_student = {}
        for student in all_students:
            if student.mac:
                mac_student[student.mac] = student
        for checkin in all_checkins:
            if not checkin.student:
                if checkin.mac in mac_student.keys():
                    checkin.student = mac_student[checkin.mac]
                    checkin.save()
