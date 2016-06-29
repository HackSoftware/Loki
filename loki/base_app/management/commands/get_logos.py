from django.core.management.base import BaseCommand
from urllib.request import urlretrieve

from base_app.models import Company


class Command(BaseCommand):
    help = 'Downloads all logos'

    def handle(self, *args, **options):
        all_companies = Company.objects.all()
        for company in all_companies:
            if company.logo:
                urlretrieve(company.logo, 'media/logos/{0}.JPG'.format(company.id))
