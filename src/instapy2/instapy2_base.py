from .configuration import Configuration

from instagrapi import Client

from os import getcwd, mkdir, path, sep
from pathlib import Path
from typing import Dict, List, Union
import urllib3

class InstaPy2Base:
    def login(self, username: str = '', password: str = '', verification_code: str = ''):
        def proxy() -> Union[None, str]:
            for proxy in self.proxies:
                try:
                    url = proxy['url'] or ''
                    username = proxy['username'] or ''
                    password = proxy['password'] or ''

                    pool = urllib3.ProxyManager(proxy_url=url, headers=urllib3.make_headers(proxy_basic_auth=f'{username}:{password}'))
                    pool.request('GET', 'https://google.com')
                    return url
                except:
                    return None

        if hasattr(self, 'proxies'):
            self.session = Client(proxy=proxy() or '')
        else:
            self.session = Client()

        if not path.exists(path=getcwd() + f'{sep}/files'):
            mkdir(path=getcwd() + f'{sep}/files')

        if path.exists(path=getcwd() + f'{sep}files{sep}{username}.json'):
            self.session.load_settings(path=getcwd() + sep + 'files' + sep + f'{username}.json') # type: ignore
            logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
        else:
            logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
            self.session.dump_settings(path=getcwd() + sep + 'files' + sep + f'{username}.json') # type: ignore

        self.configuration = Configuration(session=self.session)
        print(f'[INFO]: Successfully logged in as: {self.session.username}.' if logged_in else f'[ERROR]: Failed to log in.')

    def set_proxies(self, proxies: List[Dict[str, str]] = []):
        self.proxies = proxies