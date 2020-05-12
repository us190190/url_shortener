from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status


def get_stats(request):
    # date-wise / hour-wise
    pass
