from django.db import models


class History(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateField(auto_now_add=True)
    created_hour = models.IntegerField()
    url_id = models.IntegerField()  # Reference to Url -> id
    access_count = models.IntegerField(default=0)

    class Meta:
        db_table = "history"
