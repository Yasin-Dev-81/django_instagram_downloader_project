from .instagram import Instagram

import requests


class InstagramData(Instagram):
    def __init__(self, sessionid_list):
        super().__init__()
        self.login_with_sessionid(sessionid_list=sessionid_list)
        self.data = {}
        self.pk = None
        self.url = None
        self.media_type = 0
        self.stories = False
        self.page = False
        self.highlight = False

    def type_inspector_with_url(self, url: str, to_get: bool = True):
        if to_get:
            self.url = requests.get(url=url).url
        else:
            self.url = url
        if '/stories/' in self.url:
            print('--- type: stories')
            self.stories = True
        elif ('/p/' in self.url) or ('/reel/' in self.url) or ('/tv/' in self.url):
            print('--- type: media')
            self.stories = False
        elif '/s/' in self.url:
            print('--- type: highlight')
            self.highlight = True
        else:
            print('--- type: page')
            self.page = True

    def type_inspector_with_pk(self, pk: int, stories: bool):
        self.pk = pk
        self.stories = stories

    def data_inspector_with_url(self):
        if len(self.data) == 0:
            if self.stories:  # stories
                self.pk = self.instagram_client.story_pk_from_url(self.url)
                print('--- story pk:', self.pk)
                self.data = self.instagram_client.story_info(self.pk).dict()
            elif self.page:
                print('--- page pk:', self.pk)
            else:
                self.pk = self.instagram_client.media_pk_from_url(self.url)
                print('--- media pk:', self.pk)
                self.data = self.instagram_client.media_info(self.pk).dict()
        self.set_media_type()
        return self.data

    def data_inspector_with_pk(self):
        if len(self.data) == 0:
            if self.stories:
                print('--- story pk')
                self.data = self.instagram_client.story_info(self.pk).dict()
            elif self.page:
                print('--- page pk')
            else:
                print('--- media pk')
                self.data = self.instagram_client.media_info(self.pk).dict()
        self.set_media_type()
        return self.data

    def downloadable(self):
        if self.page or self.highlight:
            return False
        return True

    def set_media_type(self):
        self.media_type = self.data.get('media_type')
        return True
