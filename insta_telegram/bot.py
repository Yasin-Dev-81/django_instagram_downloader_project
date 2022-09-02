import requests
import telebot
from telebot import types

from insta_downloader import DirectoryDownload
from config.settings import TELEGRAM_TOKEN, MEDIA_ROOT

import os
import datetime

from django.urls import reverse
from insta_web.models import InstagramData


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
        hourglass_message = bot.reply_to(message, '\U000023F3')
        print('--- started with url:', message.text)
        insta_cl = DirectoryDownload(
            sessionid_list=[obj.sessionid for obj in InstagramData.objects.filter(active=True)],
            folder_path=os.path.join(MEDIA_ROOT, 'instagram_downloaded')
        )
        try:
            insta_cl.url = requests.get(message.text).url
            print('--- instagram url:', insta_cl.url)
            continue_process = True
        except requests.exceptions.MissingSchema:
            bot.reply_to(message, "Please send Instagram link!")
            continue_process = False
        if ("instagram.com" in insta_cl.url) and continue_process:
            insta_cl.type_inspector_with_url(insta_cl.url, to_get=False)
            print('--- typed inspected:')
            if insta_cl.downloadable():
                download_message = bot.reply_to(message, 'The download started from the Instagram server...')
                insta_cl.data_inspector_with_url()
                print('--- instagram data got from server:', insta_cl.data)
                caption_tel = """
                <i>►username:</i> <a href="https://instagram.com/{username}/">{username}</a>\n<i>📆ctime:</i> <b>{ctime}</b> 
                """.format(
                    username=insta_cl.data.get('user').get('username'),
                    ctime=insta_cl.data.get('taken_at').ctime(),
                )
                try:
                    tel_input_medias = insta_cl.input_medias(caption=caption_tel)
                    bot.send_media_group(
                        chat_id=message.chat.id,
                        media=tel_input_medias,
                        disable_notification=False,
                        protect_content=False,
                        reply_to_message_id=message.message_id,
                        allow_sending_without_reply=True,
                    )
                except Exception:
                    insta_cl.start()
                    bot.send_message(
                        chat_id=message.chat.id,
                        text="This post cannot be uploaded in Telegram, please download from the site!",
                        disable_notification=False,
                        protect_content=False,
                        reply_to_message_id=message.message_id,
                        allow_sending_without_reply=True,
                    )
                bot.delete_message(chat_id=message.chat.id, message_id=hourglass_message.message_id)
                bot.delete_message(chat_id=message.chat.id, message_id=download_message.message_id)
                # print(medias_sent)
                url_markup = types.InlineKeyboardMarkup(row_width=1)
                url_markup.add(
                    types.InlineKeyboardButton(text="open in instagram", url=message.text)
                )
                bot.send_message(
                    chat_id=message.chat.id,
                    text="<i>📃caption:</i> <code>{caption}</code>".format(caption=insta_cl.data.get('caption_text')),
                    parse_mode='html',
                    reply_markup=url_markup
                )
                bot.send_message(
                    chat_id=message.chat.id,
                    text="<i>Powered by</i> <b>{admin}</b>".format(admin='@Yasin_Dev81'),
                    parse_mode='html',
                )
            else:
                bot.reply_to(message, "This link cannot be downloaded with this robot!")
        else:
            bot.reply_to(message, "This link does not belong to Instagram!")
    except telebot.apihelper.ApiTelegramException:
        print('--- user blocked this bot!')


if __name__ == '__main__':
    bot.infinity_polling()
