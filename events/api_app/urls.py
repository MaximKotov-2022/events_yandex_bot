from django.urls import path

from .views import api_events

urlpatterns = [
    path('api/v1/events/', api_events, name='api_events'),
]
