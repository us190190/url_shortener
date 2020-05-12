import random
import string
import redis

from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Url
from .serializers import UrlSerializer


@api_view(['POST'])
def compress_url(request):
    full_url = request.POST.get('full_url', "None")
    if full_url is not None:
        # redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        new_slug = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)) # TODO fetch new slug from slug gen cached pool
        payload_serialized = {"slug": new_slug, "full_url": full_url}
        payload_serialized = UrlSerializer(data=payload_serialized)
        if payload_serialized.is_valid():
            payload_serialized.save()
            return JsonResponse(payload_serialized.data, status=status.HTTP_201_CREATED, safe=False)
        else:
            return JsonResponse(payload_serialized.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
    else:
        return JsonResponse({"error": "full_url cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def fetch_url(request):
    slug = request.GET.get('slug', None)
    if slug is not None:
        url_data = Url.objects.get(slug=slug)
        url_data_serialized = UrlSerializer(url_data)
        # TODO add data for total_access_count and date+hour level count
        # TODO put this into service call
        return JsonResponse(url_data_serialized.data)
    else:
        return JsonResponse({"error": "slug cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_url(request):
    keyword = request.GET.get('keyword', None)
    limit = request.GET.get('limit', 5)
    if keyword is not None:
        urls = Url.objects.all()  # TODO orderby created_at, frequency
        suggestions = []
        for url in urls:
            if keyword in url.full_url:  # TODO have to do pattern matching
                suggestions.append(url)
                if len(suggestions) == int(limit):
                    break
        suggestions_serialized = UrlSerializer(suggestions, many=True)
        return JsonResponse(suggestions_serialized.data, safe=False)
    else:
        return JsonResponse({"error": "keyword cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST)
