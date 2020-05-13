from django.core.management.base import BaseCommand

from django.apps import apps

History = apps.get_model("analytics", "History")


class Command(BaseCommand):
    help = 'Persist stats in database. This is an hourly script to be update access history of URLs.'

    def handle(self, *args, **kwargs):
        print(History.persist_stats_from_redis())
