from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from .bot import bot as tbot
import telebot


@csrf_exempt
def webhook_view(request):
    if request.META['CONTENT_TYPE'] == 'application/json':

        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])

        return HttpResponse("")
    else:
        if request.user.is_staff:
            webhook_url = request.build_absolute_uri()
            tbot.remove_webhook()
            tbot.set_webhook(webhook_url)
            return HttpResponse(f"set webhook: {webhook_url}")
        else:
            raise PermissionDenied
