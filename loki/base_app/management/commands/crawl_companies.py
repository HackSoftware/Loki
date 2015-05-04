from django.core.management.base import BaseCommand, CommandError

from requests import get
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

from base_app.models import Company


class Command(BaseCommand):
    help = 'Crawls all IT companies from jobs.bg'

    def handle(self, *args, **options):
        company_id = 213917
        home_title = 'jobs.bg - Предложения за работа от водещи компании в България'

        while company_id > 0:
            try:
                url = 'http://www.jobs.bg/company/{0}'.format(company_id)
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

                    Company.objects.create(
                        name=name,
                        logo=image_link,
                        jobs_link=url,
                    )
                    print(company_id)
            except ConnectionError as err:
                pass
            company_id -= 1
