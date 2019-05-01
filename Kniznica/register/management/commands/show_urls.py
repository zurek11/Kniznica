from django.conf import settings
from django.core.management import BaseCommand
from django.urls import get_resolver

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])


class Command(BaseCommand):
    def handle(self, **options):
        for item in set(v[1] for k, v in get_resolver(None).reverse_dict.items()):
            print(item)
