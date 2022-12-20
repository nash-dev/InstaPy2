from .configuration import Configuration

from instagrapi import Client

from os import getcwd, mkdir, path, sep
from random import choice
from typing import List

class InstaPy2Base:
    def login(self, username: str = '', password: str = '', verification_code: str = ''):
        if hasattr(self, 'proxies'):
            proxy = choice(seq=self.proxies)
            self.session = Client(proxy=proxy)
            print(f'[INFO]: Created session using proxy: {proxy}.')
        else:
            self.session = Client()
            print('[INFO]: Created session without proxy.')

        if not path.exists(path=getcwd() + f'{sep}/files'):
            mkdir(path=getcwd() + f'{sep}/files')
            print('[INFO]: Created files directory.')

        if path.exists(path=getcwd() + sep + 'files' + sep + f'{username}.json'):
            self.session.load_settings(path=getcwd() + sep + 'files' + sep + f'{username}.json') # type: ignore
            logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
        else:
            logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
            self.session.dump_settings(path=getcwd() + sep + 'files' + sep + f'{username}.json') # type: ignore

        self.configuration = Configuration(session=self.session)
        print(f'[INFO]: Successfully logged in as: {self.session.username}.' if logged_in else '[ERROR]: Failed to log in.')

    def set_proxies(self, proxies: List[str] = []):
        self.proxies = proxies