from django.core.management.base import BaseCommand
from education.models import CheckIn, Student


class Command(BaseCommand):
    help = 'Assign names to nameless macs'

    def handle(self, *args, **options):
        all_students = Student.objects.all()
        all_checkins = CheckIn.objects.all()

        mac_student = {}
        for student in all_students:
            if student.mac:
                mac_student[student.mac.lower()] = student

        for checkin in all_checkins:
            if not checkin.student:
                if checkin.mac.lower() in mac_student.keys():
                    try:
                        checkin.student = mac_student[checkin.mac.lower()]
                        checkin.save()
                    except Exception as error:
                        print(error)
