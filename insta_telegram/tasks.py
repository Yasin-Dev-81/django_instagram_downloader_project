import os
import requests
import datetime

import telebot
from telebot import types

from config.settings import MEDIA_ROOT
from insta_downloader import DirectoryDownload
from insta_web import models


class TelTasksForInstaLink:
    def __init__(self, bot, message):
        # message's
        self.download_message = None
        self.hourglass_message = None
        self.message = message
        # client's
        self.bot = bot
        self.insta_cl = DirectoryDownload(
            sessionid_list=[obj.sessionid for obj in models.InstagramData.objects.filter(active=True)],
            folder_path=os.path.join(MEDIA_ROOT, 'instagram_downloaded')
        )
        self.url = None

    def send_hourglass_message(self):
        self.hourglass_message = self.bot.reply_to(self.message, '\U000023F3')

    def valid_url(self):
        try:
            self.url = requests.get(self.message.text).url
            if "instagram.com" in self.url:
                self.insta_cl.url = self.url
                print('--- instagram url:', self.insta_cl.url)
                return True
            else:
                self.bot.reply_to(self.message, "This link does not belong to Instagram!")
                raise ValueError('Not a Instagram url!')
        except requests.exceptions.MissingSchema:
            self.bot.reply_to(self.message, "Please send Instagram url!")
            raise ValueError('Not a url!')

    def inspect_type_and_data(self):
        self.insta_cl.type_inspector_with_url(self.insta_cl.url, to_get=False)
        if self.insta_cl.downloadable():
            self.download_message = self.bot.reply_to(self.message, 'The download started from the Instagram server...')
            self.insta_cl.data_inspector_with_url()
        else:
            self.message.reply_to(self.message, "This link cannot be downloaded with this robot!")
            raise ValueError('This link cannot be downloaded with this robot!')

    def send_medias(self):
        tel_input_medias = self.insta_cl.input_medias()
        try:
            self.bot.send_media_group(
                chat_id=self.message.chat.id,
                media=tel_input_medias,
                disable_notification=False,
                protect_content=False,
                reply_to_message_id=self.message.message_id,
                allow_sending_without_reply=True,
            )
        except telebot.apihelper.ApiTelegramException:
            for tel_input_media in tel_input_medias:
                self.bot.send_media_group(
                    chat_id=self.message.chat.id,
                    media=tel_input_media,
                    disable_notification=False,
                    protect_content=False,
                    reply_to_message_id=self.message.message_id,
                    allow_sending_without_reply=True,
                )

    def send_captions(self):
        caption_tel = """
        <i>►username:</i> <a href="https://instagram.com/{username}/">{username}</a>\n<i>📆ctime:</i> <b>{ctime}</b> 
        """.format(
            username=self.insta_cl.data.get('user').get('username'),
            ctime=self.insta_cl.data.get('taken_at').ctime(),
        )
        self.bot.send_message(
            chat_id=self.message.chat.id,
            text=caption_tel,
            parse_mode='html',
        )
        url_markup = types.InlineKeyboardMarkup(row_width=1)
        url_markup.add(
            types.InlineKeyboardButton(text="open in instagram", url=self.url)
        )
        self.bot.send_message(
            chat_id=self.message.chat.id,
            text="<i>📃caption:</i> <code>{caption}</code>".format(caption=self.insta_cl.data.get('caption_text')),
            parse_mode='html',
            reply_markup=url_markup
        )

    def send_powered(self):
        self.bot.send_message(
            chat_id=self.message.chat.id,
            text="<i>Powered by</i> <b>{admin}</b>".format(admin='@Yasin_Dev81'),
            parse_mode='html',
        )

    def delete_additions_messages(self):
        self.bot.delete_message(
            chat_id=self.message.chat.id,
            message_id=self.hourglass_message.message_id
        )
        self.bot.delete_message(
            chat_id=self.message.chat.id,
            message_id=self.download_message.message_id
        )
