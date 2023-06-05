from rest_framework import serializers
from .models import Events


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('date', 'name', 'site')
        model = Events
