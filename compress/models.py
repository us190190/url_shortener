
from django.db import models
from django_redis import get_redis_connection
redis_default_connection = get_redis_connection("default")
redis_stats_connection = get_redis_connection("stats")

class Url(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(unique=True, max_length=6)  # 26^6 308915776 unique values consisting of a-z
    full_url = models.URLField()  # max_length = 255
    visited_total_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "url"

    @staticmethod
    def get_url(slug):

        value = redis_default_connection.get(slug)
        if value is None:
            try:
                url_data = Url.objects.get(slug=slug)
            except Url.DoesNotExist:
                return None
            value = url_data.full_url
            redis_default_connection.set(slug, value)

        # TODO add data for total_access_count and date+hour level count
        # TODO put this into service call
        return value

    @staticmethod
    def get_suggestions(keyword, limit):
        return Url.objects.filter(full_url__contains=keyword).order_by("-visited_total_count")[:int(limit)]


