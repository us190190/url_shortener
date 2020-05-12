from django.conf.urls import url
from .views import compress_url, fetch_url, search_url

urlpatterns = [
    url(r'^api/compress$', compress_url),
    url(r'^api/fetch$', fetch_url),
    url(r'^api/search$', search_url)
]
