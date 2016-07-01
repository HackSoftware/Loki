import csv

from random import randint
from django.core.management.base import BaseCommand
from django.conf import settings
from post_office import mail

from education.models import Student, CourseAssignment, Course


class Command(BaseCommand):
    args = '<path_to_csv_file>'
    help = '''
        I will import users from the csv file.
        I will generate random passwords and send emails to them.
        You can edit the email template located in students/management/commands/template.txt
        The format of the CSV file must be:
            email, first_name last_name, 1/2, course_id, skype, phone
        * 1 is for early group_time
        * 2 is for late group_time
        !!IMPORTANT: your emails and names must not contain comma [,].
        We use the comma for value separation!
        May the force be with you!
    '''

    def handle(self, *args, **options):
        with open(args[0], 'r') as csvfile:
            csv_line = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csv_line:
                email = row[0]
                full_name = row[1].strip()
                first_name = full_name.split()[0]
                last_name = full_name.split()[-1]
                group_time = row[2].strip()
                course_id = row[3].strip()
                skype = row[4].strip()
                phone = row[5].strip()
                new_password = 'You know your password!'

                current_course = Course.objects.get(id=course_id)
                if not current_course:
                    raise Exception('Invalid course given for' + email)

                new_user, created = Student.objects.get_or_create(
                    email=email,
                )

                if created:
                    new_password = randint(1000000000, 9999999999)
                    new_user.set_password(new_password)

                    new_user.first_name = first_name
                    new_user.last_name = last_name

                    new_user.skype = skype
                    new_user.phone = phone
                    new_user.is_active = True
                    new_user.save()

                    sender = settings.EMAIL_HOST_USER
                    mail.send(
                        new_user.email,
                        sender,
                        template='new_account_generated',
                        context={
                            'full_name': new_user.full_name,
                            'password': new_password,
                            'email': email
                        }
                    )

                CourseAssignment.objects.get_or_create(
                    user=new_user,
                    course=current_course,
                    group_time=group_time
                )

                print(full_name + ' registered successfully')
