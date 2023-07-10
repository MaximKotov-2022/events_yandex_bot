from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from events.bot_main import GetData

from .serializers import EventsSerializer


@api_view(['GET'])
def api_events(request):
    if request.method == 'GET':
        data = GetData.processing_data_website()

        serializer = EventsSerializer(data=data, many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
