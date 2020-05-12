import string
from random import random

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status


# Create your views here.

def check_sufficient_slugs():
    new_slug = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)) # TODO fetch new slug from slug gen cached pool
