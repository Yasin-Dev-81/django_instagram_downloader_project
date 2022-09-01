import requests
import telebot
from telebot import types

from insta_downloader import DirectoryDownload
from config.settings import TELEGRAM_TOKEN, MEDIA_ROOT

import os
import datetime


bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message)
    bot.reply_to(message, "Howdy, how are you doing? \U000023F3")


@bot.message_handler(func=lambda message: True)
def instagram(message):
    hourglass_message = bot.reply_to(message, '\U000023F3')
    print('--- started with url:', message.text)
    insta_cl = DirectoryDownload(
        sessionid_list=[obj.sessionid for obj in InstagramData.objects.filter(active=True)],
        folder_path=os.path.join(settings.MEDIA_ROOT, 'instagram_downloaded')
    )
    try:
        insta_cl.url = requests.get(message.text).url
        continue_process = True
    except requests.exceptions.MissingSchema:
        bot.reply_to(message, "Please send Instagram link!")
        continue_process = False
    if ("instagram.com" in insta_cl.url) and continue_process:
        insta_cl.type_inspector_with_url(insta_cl.url, to_get=False)
        if insta_cl.downloadable():
            download_message = bot.reply_to(message, 'The download started from the Instagram server...')
            insta_cl.data_inspector_with_url()
            print(insta_cl.data)
            caption_tel = """
            <i>►username:</i> <a href="https://instagram.com/{username}/">{username}</a>\n<i>📆ctime:</i> <b>{ctime}</b> 
            """.format(
                username=insta_cl.data.get('user').get('username'),
                ctime=insta_cl.data.get('taken_at').ctime(),
            )
            medias_sent = bot.send_media_group(
                chat_id=message.chat.id,
                media=insta_cl.input_medias(caption=caption_tel),
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


bot.infinity_polling()
