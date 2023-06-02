import json

from django.http import JsonResponse
from rest_framework.decorators import api_view

from events.bot_main import GetData


@api_view(['GET'])
def api_events(request):
    if request.method == 'GET':
        data = json.dumps(
            {'events': (GetData.processing_data_website())}
        )

        return JsonResponse(json.loads(data), safe=False)
