from django.db import models


class Url(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(unique=True, max_length=6)  # 26^6 308915776 unique values consisting of a-z
    full_url = models.URLField()  # max_length = 255
    visited_total_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "url"



