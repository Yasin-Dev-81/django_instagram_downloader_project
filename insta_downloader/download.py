import time
import zipfile
from .zip_dir import zipdir

from urllib import request
import threading
import os

from .data import InstagramData
from .instagram import Instagram

from telebot import types


class DirectoryDownload(InstagramData, Instagram, threading.Thread):
    def __init__(self, folder_path, sessionid_list: list):
        super().__init__(sessionid_list=sessionid_list)
        self.zip_path = None
        self.pk_folder_path = None
        self.main_folder_path = folder_path
        self.resources = []

    def is_downloaded(self):
        if os.path.exists(self.pk_folder_path):
            files_list = os.listdir(self.pk_folder_path)
            if len(files_list) == 0:
                return False
            else:
                return True

    def get_resources(self):
        if len(self.data) == 0:
            self.data_inspector_with_url()
        if self.media_type == 0:
            self.set_media_type()
        print('---', self.media_type)
        resources = []
        if self.media_type == 1:  # photo
            resource_dict = {
                'pk': self.pk,
                'url': self.data.get('thumbnail_url').__str__(),
                'path': os.path.join(self.pk_folder_path, '%s.jpg' % (self.pk,)),
                'media_type': 1
            }
            resources.append(resource_dict)
        elif self.media_type == 2:  # video
            resource_dict = {
                'pk': self.pk,
                'url': self.data.get('video_url').__str__(),
                'path': os.path.join(self.pk_folder_path, '%s.mp4' % (self.pk,)),
                'media_type': 2
            }
            resources.append(resource_dict)
        else:  # multy
            i = 0
            for resource in dict(self.data).get('resources'):
                i += 1
                if resource.get('media_type') == 1:  # photo
                    resource_dict = {
                        'pk': resource.get('pk'),
                        'url': resource.get('thumbnail_url').__str__(),
                        'path': os.path.join(self.pk_folder_path, '%s - %s.jpg' % (i, resource.get('pk'),)),
                        'media_type': 1
                    }
                else:  # video
                    resource_dict = {
                        'pk': resource.get('pk'),
                        'url': resource.get('video_url').__str__(),
                        'path': os.path.join(self.pk_folder_path, '%s - %s.mp4' % (i, resource.get('pk'),)),
                        'media_type': 2
                    }
                resources.append(resource_dict)
        self.resources = resources
        return self.resources
    
    def download(self):
        self.pk_folder_path = os.path.join(self.main_folder_path, str(self.pk))
        if self.is_downloaded():
            print('---- The file has already been downloaded')
        elif self.page:
            pass
        elif len(self.resources) == 0:
            self.get_resources()
        else:
            # create folder
            if not os.path.exists(self.pk_folder_path):
                os.mkdir(str(self.pk_folder_path))
            # download
            resource_path_list = []
            for resource in self.resources:
                request.urlretrieve(resource.get('url'), resource.get('path'))
                resource_path_list.append(resource.get('path'))
                print('--- downloaded:', resource.get('path'))
            else:
                return resource_path_list

    def input_medias(self, caption: str = '', parse_mode: str = 'html'):
        capt = False
        input_medias = []
        self.get_resources()
        for resource in self.resources:
            if resource.get('media_type') == 1:
                if capt:
                    input_medias.append(
                        types.InputMediaPhoto(resource.get('url'))
                    )
                else:
                    input_medias.append(
                        types.InputMediaPhoto(
                            resource.get('url'),
                            caption=caption,
                            parse_mode=parse_mode
                        )
                    )
                    capt = True
            elif resource.get('media_type') == 2:
                if capt:
                    input_medias.append(
                        types.InputMediaVideo(resource.get('url'))
                    )
                else:
                    input_medias.append(
                        types.InputMediaVideo(
                            resource.get('url'),
                            caption=caption,
                            parse_mode=parse_mode
                        )
                    )
            time.sleep(0.5)
        else:
            return input_medias

    def zip_download(self):
        self.zip_path = os.path.join(self.main_folder_path, '%s.zip' % self.pk)
        if self.zip_is_downloaded():
            print('---- The file has already been downloaded')
        else:
            if not self.is_downloaded():
                self.download()
            with zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipdir(
                    self.pk_folder_path,
                    zipf
                )

    def zip_is_downloaded(self):
        return os.path.exists(self.zip_path)

    def start(self) -> None:
        self.download()
        self.zip_download()
