from django.core.management.base import BaseCommand
from django_redis import get_redis_connection

from django.conf import settings
from django.apps import apps
Slug = apps.get_model("sluggen", "Slug")


class Command(BaseCommand):
    help = 'Populate slugs in redis. This is service which has to be run daily or twice a day.'

    def handle(self, *args, **kwargs):

        redis_slugs_connection = get_redis_connection("slugs")
        current_slugs_count = redis_slugs_connection.llen("available_slugs")

        diff = int(settings.SLUGS_IN_REDIS_COUNT) - int(current_slugs_count)

        if diff > 0:
            print(Slug.populate_slugs_in_redis(diff))
        else:
            print("Redis already has " + str(current_slugs_count) + " slugs")
