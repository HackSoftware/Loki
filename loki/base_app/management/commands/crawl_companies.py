from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from requests import get
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

from base_app.models import Company


class Command(BaseCommand):
    args = '<number>'
    help = 'Crawls all IT companies from jobs.bg'

    def handle(self, *args, **options):
        # Last ID for the end of april 2015
        end_id = 0
        company_id = 213917
        company_id_updated = company_id
        if len(args):
            if Company.objects.all().count() == 0:
                print("Database does not exist. Run command without arguments first")
                return
            else:
                company_id_updated = company_id + int(args[0])
                end_id = company_id
        home_title = 'jobs.bg - Предложения за работа от водещи компании в България'
        while company_id_updated > end_id:
            try:
                url = 'http://www.jobs.bg/company/{0}'.format(company_id_updated)
                info = get(url)
                info.encoding = 'utf-8'
                html = info.text
                soup = BeautifulSoup(html)
                if 'Информационни' in html and soup.title.string != home_title:
                    name = soup.title.string
                    links = soup.findAll('img')
                    image_link = ''
                    for link in links:
                        if 'logo' in link['src'] and 'assets' in link['src']:
                            image_link = link['src']
                    try:
                        Company.objects.create(
                            name=name,
                            logo=image_link,
                            jobs_link=url,
                        )
                    except IntegrityError:
                        pass
                    # print(company_id_updated)
            except ConnectionError:
                pass
            company_id_updated -= 1
