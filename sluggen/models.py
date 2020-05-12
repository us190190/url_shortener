from django.db import models


class Slug(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(unique=True, max_length=6)  # 26^6 308915776 unique values consisting of a-z
    created_at = models.DateTimeField(auto_now_add=True)
    consumed = models.BooleanField(default=False)

    class Meta:
        db_table = "slug"
