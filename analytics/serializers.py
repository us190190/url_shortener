from rest_framework import serializers
from .models import History


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = ('slug',
                  'created_date',
                  'created_hour',
                  'access_count')
