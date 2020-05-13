import random
import string

from django.db import models


class Slug(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(unique=True, max_length=6)  # 26^6 308915776 unique values consisting of a-z
    created_at = models.DateTimeField(auto_now_add=True)
    consumed = models.BooleanField(default=False)

    class Meta:
        db_table = "slug"

    @staticmethod
    def get_new():
        # TODO have to pop this from SPOP
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
                       range(6))  # TODO fetch new slug from slug gen cached pool
