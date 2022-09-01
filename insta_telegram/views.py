from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from .bot import bot as tbot
import telebot


# webhook
@csrf_exempt
def webhook_view(request):
    print('--- request meta:', request.META)
    if request.META.get('CONTENT_TYPE') == 'application/json':
        print('--- got data from telegram.')
        
        json_data = request.body.decode('utf-8')
        print('--- json data:', json_data)
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])
        print('--- telebot is updated.')

        return HttpResponse("")
    else:
        if request.user.is_staff:
            webhook_url = request.build_absolute_uri()
            tbot.remove_webhook()
            tbot.set_webhook(webhook_url)
            return HttpResponse(f"set webhook: {webhook_url}")
        else:
            print('--- else-else!')
            raise PermissionDenied
