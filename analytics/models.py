from datetime import datetime

from django.db import models
from django_redis import get_redis_connection

redis_stats_connection = get_redis_connection("stats")


class History(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateField(auto_now_add=True)
    created_hour = models.IntegerField()
    slug = models.CharField(max_length=6, null=False)  # Reference to Url -> slug
    access_count = models.IntegerField(default=0)

    class Meta:
        db_table = "history"

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
        today = now_utc.strftime('%Y-%m-%d')
        for hour in range(current_hour+1):
            pattern = str(hour) + "_*"
            urls_stats = redis_stats_connection.keys(pattern)
            for url_stats in urls_stats:
                key = url_stats.decode('utf-8')
                (request_hour, slug) = key.split("_")
                count = redis_stats_connection.get(key).decode('utf-8')
                print(request_hour)
                print(count)


