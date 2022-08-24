from instagrapi import Client
from instagrapi.exceptions import LoginRequired

from random import shuffle


class Instagram:
    def __init__(self):
        self.instagram_client = Client()

    def login_with_sessionid(self, sessionid_list: list):
        shuffle(sessionid_list)
        for sessionid in sessionid_list:
            try:
                self.instagram_client.login_by_sessionid(sessionid=sessionid)
                print('--- logged in with sessionid:', sessionid)
                break
            except LoginRequired or AttributeError:
                continue
        else:
            print('--- Not logged in!')
            return False
        return True

    def login_with_settings(self, settings: dict):
        self.instagram_client.set_settings(settings=settings)
        self.instagram_client.login_flow()
        print('--- logged in with flow')
        return True
