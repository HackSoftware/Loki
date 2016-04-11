import json
import time

from random import randint
from django.core.management.base import BaseCommand
from django.conf import settings
from post_office import mail

from education.models import Student, CourseAssignment, Course


class Command(BaseCommand):
    args = '<path_to_json_file>'
    help = '''
    This command imports students to a given course from a JSON file.
    Students are created with a random password. In order to log in, they must use password reset.
    The format of the file is as follows:
    {
        'course_id': 1,
        'students': [{
            'first_name': 'Panda',
            'last_name': 'Panda',
            'email': 'panda@panda.com',
            'group_time': 1
        },
        ...
        ]
    }
    '''

    def add_arguments(self, parser):
        parser.add_argument('students', type=str)

    def handle(self, *args, **options):
        with open(options['students'], 'r') as f:
            data = json.load(f)

        course = Course.objects.get(pk=data['course_id'])

        for student in data['students']:
            obj, created = Student.objects.get_or_create(email=student['email'])

            if created:
                new_password = randint(1000000000, 9999999999)
                obj.set_password(new_password)

                obj.first_name = student['first_name']
                obj.last_name = student['last_name']

                obj.is_active = True
                obj.save()

                sender = settings.EMAIL_HOST_USER
                mail.send(
                    obj.email,
                    sender,
                    template='new_account_generated',
                    context={
                        'full_name': obj.full_name,
                        'email': student['email']
                    }
                )

            CourseAssignment.objects.get_or_create(
                user=obj,
                course=course,
                group_time=student['group_time']
            )

            print(student['email'] + ' registered successfully')
