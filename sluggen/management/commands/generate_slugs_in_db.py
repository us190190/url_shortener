from django.core.management.base import BaseCommand

from django.apps import apps

Slug = apps.get_model("sluggen", "Slug")


class Command(BaseCommand):
    help = 'Generate slugs in database. This is a one time script to be run once in a year.'

    def handle(self, *args, **kwargs):
        print(Slug.generate_slugs_in_db())
