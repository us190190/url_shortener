from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import HistorySerializer

from django.apps import apps

History = apps.get_model("analytics", "History")


@api_view(['GET'])
def get_stats(request):
    date = request.GET.get('date', None)
    if date is not None:
        stats = History.get_stats_by_date(date=date)
        stats_serialized = HistorySerializer(stats, many=True)
        return JsonResponse(stats_serialized.data, safe=False)
    else:
        return JsonResponse({"error": "date cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST)
