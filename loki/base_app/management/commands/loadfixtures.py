from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps

import json
import os

FIXTURE_FOLDER = 'fixtures'
CURRENT_APP = __name__.split('.')[0]


def is_fk(model):
    return len(model.split('.')) > 1


def get_model_instance(parts, value):
    app_label, model_name = parts[:2]
    Model = apps.get_model(app_label=app_label, model_name=model_name)

    # If there are two parts, then seek by PK
    if len(parts) == 2:

        return Model.objects.get(pk=value)

    # If there are three parts, seek by the given field
    if len(parts) == 3:
        query = {}
        query[parts[2]] = value
        return Model.objects.get(**query)


class Command(BaseCommand):
    args = '<fixture>'
    help = 'Load given fixture more intelligently than Django. Supports only JSON.'

    def add_arguments(self, parser):
        parser.add_argument('fixture', type=str)

    def handle(self, *args, **options):
        fixture = options['fixture']
        path = os.path.join(settings.BASE_DIR,
                            CURRENT_APP,
                            FIXTURE_FOLDER,
                            fixture)

        with open(path, 'r') as f:
            data = json.load(f)

        for item in data:
            model = item['model']
            app_label, model_name = model.split('.')

            Model = apps.get_model(app_label=app_label, model_name=model_name)
            m = Model()

            for key, value in item['fields'].items():
                if is_fk(key):
                    parts = key.split('.')
                    obj = get_model_instance(parts, value)
                    setattr(m, parts[1], obj)
                else:
                    setattr(m, key, value)
            print(m)
            m.save()
