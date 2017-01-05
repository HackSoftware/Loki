from django.core.management.base import BaseCommand
from django.conf import settings
from loki.hack_fmi.models import BlackListToken
from ...helper import get_date_with_timedelta


class Command(BaseCommand):
    help = 'Clean jwt tokens which are older than 1 week'

    def handle(self, *args, **options):
        days = settings.JWT_AUTH['JWT_EXPIRATION_DELTA'].days
        blacklisted_dates = get_date_with_timedelta(days=-days)
        BlackListToken.objects.filter(created_at__lte=blacklisted_dates).delete()
        print("BlackListTokens deleted.")
