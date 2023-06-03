from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import EventsSerializer
from events.bot_main import GetData


@api_view(['GET'])
def api_events(request):
    if request.method == 'GET':
        data = GetData.processing_data_website()

        serializer = EventsSerializer(data=data, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)
