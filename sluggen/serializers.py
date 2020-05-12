from rest_framework import serializers
from .models import Slug


class SlugSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slug
        fields = ('slug',
                  'created_at',
                  'consumed')
