from django.conf.urls import url
from .views import get_stats

urlpatterns = [
    url(r'^api/stats$', get_stats),
]
