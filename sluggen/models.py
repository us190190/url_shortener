import random
import string
import time

from django.db import models
from django.conf import settings
from django_redis import get_redis_connection

redis_slugs_connection = get_redis_connection("slugs")


class Slug(models.Model):
    slug = models.CharField(unique=True, max_length=6)  # 26^6 308915776 unique values consisting of a-z
    created_at = models.DateTimeField(auto_now_add=True)
    consumed = models.BooleanField(default=False)

    class Meta:
        db_table = "slug"

    @staticmethod
    def generate_slugs_in_db():

        batch_size = settings.POPULATE_SLUGS_DB_BATCH_SIZE
        chunk_size = 500
        total = batch_size

        while batch_size:
            slugs = []
            chunk_size = batch_size if batch_size < chunk_size else chunk_size
            while len(slugs) < chunk_size:
                value = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
                                range(6))
                try:
                    Slug.objects.create(slug=value)
                except Exception as e:
                    continue
                slugs.append(value)
            time.sleep(5)  # sleep for 5 seconds
            batch_size -= chunk_size

        return str(total) + " slugs inserted in database successfully!"

    @staticmethod
    def populate_slugs_in_redis(count=0):

        available_slugs = Slug.objects.filter(consumed=False)[:count]
        sleep_after = 200
        counter = 0

        for available_slug in available_slugs:
            counter += 1
            slug_value = available_slug.slug
            available_slug.consumed = True
            available_slug.save()
            redis_slugs_connection.rpush("available_slugs", slug_value)
            if counter == sleep_after:
                time.sleep(5)  # sleep for 5 seconds
                counter = 0

        return str(count) + " slugs inserted in redis successfully!"

    @staticmethod
    def get_new():
        fresh_slug = redis_slugs_connection.rpop("available_slugs").decode('utf-8')
        if fresh_slug:
            return fresh_slug
        else:
            Slug.populate_slugs_in_redis(settings.SLUGS_IN_REDIS_COUNT)
            return redis_slugs_connection.rpop("available_slugs").decode('utf-8')
