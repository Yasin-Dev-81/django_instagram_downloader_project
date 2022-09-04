import os

import instagrapi
import telebot

from config.settings import TELEGRAM_TOKEN, MEDIA_ROOT
from insta_downloader import DirectoryDownload
from insta_web.models import InstagramData
from .tasks import TelTasksForInstaLink


bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message)
    bot.reply_to(
        message,
        "Howdy {name},\nEnter the URL to the post, story or highlight and I'll download it for you.".format(
            name=message.chat.first_name
        )
    )
    if __name__ != '__main__':
        pass


@bot.message_handler(func=lambda message: True)
def instagram(message):
    try:
        cl = TelTasksForInstaLink(bot, message)
        cl.valid_url()
        cl.send_hourglass_message()
        cl.inspect_type_and_data()
        cl.send_medias()
        cl.delete_additions_messages()
        cl.send_captions()
        cl.send_powered()
    except ValueError:
        print('--- error:', ValueError)
    except telebot.apihelper.ApiTelegramException:
        print('--- user blocked this bot!')


if __name__ == '__main__':
    bot.infinity_polling()
