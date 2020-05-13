from datetime import datetime

from django.db import models
from django.apps import apps
from django_redis import get_redis_connection

redis_stats_connection = get_redis_connection("stats")


class History(models.Model):
    created_date = models.DateField(auto_now_add=True)
    created_hour = models.IntegerField()
    slug = models.CharField(max_length=6, null=False)  # Reference to Url -> slug
    access_count = models.IntegerField(default=0)

    class Meta:
        db_table = "history"
        unique_together = ["created_date", "created_hour", "slug"]
        indexes = [
            models.Index(fields=["created_date", "created_hour"], name='date_hour_slug_idx'),
            models.Index(fields=["created_date"], name='date_idx'),
        ]

    @staticmethod
    def count_requested(slug):
        now_utc = datetime.utcnow()
        hour = now_utc.hour
        key = str(hour) + "_" + slug
        redis_stats_connection.incr(key)

    @staticmethod
    def persist_stats_from_redis():
        now_utc = datetime.utcnow()
        current_hour = now_utc.hour
        Url = apps.get_model("compress", "Url")
        for hour in range(current_hour):
            pattern = str(hour) + "_*"
            urls_stats = redis_stats_connection.keys(pattern)
            for url_stats in urls_stats:
                key = url_stats.decode('utf-8')
                (request_hour, slug) = key.split("_")
                count = redis_stats_connection.get(key).decode('utf-8')
                History.objects.create(created_hour=request_hour, slug=slug, access_count=count)
                url_obj = Url.objects.get(slug=slug)
                url_obj.visited_total_count += int(count)
                url_obj.save()
                redis_stats_connection.delete(key)

    @staticmethod
    def get_stats_by_date(date):
        return History.objects.filter(created_date=date).order_by("created_hour")


