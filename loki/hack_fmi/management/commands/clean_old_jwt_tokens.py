from django.core.management.base import BaseCommand
from loki.hack_fmi.models import BlackListToken
from ...helper import get_date_with_timedelta


class Command(BaseCommand):
    help = 'Clean jwt tokens which are older than 1 week'

    def handle(self, *args, **options):
        older_than_one_week = get_date_with_timedelta(days=-7)
        BlackListToken.objects.filter(created_at__lte=older_than_one_week).delete()
        print("BlackListTokens deleted.")
