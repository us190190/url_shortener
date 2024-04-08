from django.urls import re_path
from .views import get_stats

urlpatterns = [
    re_path(r'^api/stats$', get_stats),
]
