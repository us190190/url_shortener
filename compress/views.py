from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Url
from .serializers import UrlSerializer

from django.apps import apps

Slug = apps.get_model("sluggen", "Slug")


@api_view(['POST'])
def compress_url(request):
    full_url = request.POST.get('full_url', "None")
    if full_url is not None:
        try:
            new_slug = Slug.get_new()
            url_object = Url.objects.create(slug=new_slug, full_url=full_url)
            url_serialized = UrlSerializer(url_object)
            return JsonResponse(url_serialized.data, status=status.HTTP_201_CREATED, safe=False)
        except Exception as e:
            return JsonResponse({"error": "Couldn't process your request. PLease try after sometime."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"error": "full_url cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def fetch_url(request):
    slug = request.GET.get('slug', None)
    if slug is not None:
        value = Url.get_url(slug=slug)
        if value is None:
            return JsonResponse({"error": "slug doesn't exist!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"full_url": value})
    else:
        return JsonResponse({"error": "slug cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_url(request):
    keyword = request.GET.get('keyword', None)
    limit = request.GET.get('limit', 5)
    if keyword is not None:
        urls = Url.get_suggestions(keyword=keyword, limit=limit)
        suggestions_serialized = UrlSerializer(urls, many=True)
        return JsonResponse(suggestions_serialized.data, safe=False)
    else:
        return JsonResponse({"error": "keyword cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST)
