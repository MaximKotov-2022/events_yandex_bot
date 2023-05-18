import json

from django.http import JsonResponse

from events.bot_main import GetData


def api_view(request):
    if request.method == 'GET':
        data = json.dumps(
            {'events': (GetData.processing_data_website())}
        )

        return JsonResponse(json.loads(data), safe=False)
