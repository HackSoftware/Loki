from datetime import datetime
from django.core.management.base import BaseCommand
from education.models import CheckIn


class Command(BaseCommand):
    help = 'Check if at least one check in is in DB'

    def handle(self, *args, **options):
        date = datetime.now().date()
        if CheckIn.objects.filter(date=date).count():
            return True
        return False
