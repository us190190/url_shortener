from django.urls import re_path
from .views import compress_url, fetch_url, search_url

urlpatterns = [
    re_path(r'^api/compress$', compress_url),
    re_path(r'^api/fetch$', fetch_url),
    re_path(r'^api/search$', search_url)
]
