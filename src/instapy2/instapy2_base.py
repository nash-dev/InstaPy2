from .configuration import Configuration

from instagrapi import Client

from os import getcwd, mkdir, path
from typing import Dict, List, Union
import urllib3

class InstaPy2Base:
    def login(self, username: str = None, password: str = None, verification_code: str = ''):
        def proxy() -> Union[None, str]:
            if self.proxies is None:
                return None
            else:
                for proxy in self.proxies:
                    try:
                        url = proxy['url'] or ''
                        username = proxy['username'] or ''
                        password = proxy['password'] or ''

                        pool = urllib3.ProxyManager(proxy_url=url, headers=urllib3.make_headers(proxy_basic_auth=f'{username}:{password}'))
                        pool.request('GET', 'https://google.com')
                        return proxy
                    except:
                        return None

        self.session = Client(proxy=proxy())

        if not path.exists(path=getcwd() + f'{path.sep}/files'):
            mkdir(path=getcwd() + f'{path.sep}/files')

        if path.exists(path=getcwd() + f'{path.sep}files{path.sep}{username}.json'):
            self.session.load_settings(path=getcwd() + f'{path.sep}files{path.sep}{username}.json')
            logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
        else:
            logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
            self.session.dump_settings(path=getcwd() + f'{path.sep}files{path.sep}{username}.json')

        print(f'[INFO]: Successfully logged in as: {self.session.username}.' if logged_in else f'[ERROR]: Failed to log in.')
        self.configuration = Configuration(session=self.session)

    def set_proxies(self, proxies: List[Dict[str, str]] = None):
        self.proxies = proxies

"""

[
    {
        'url' : 'https://address:port',
        'username' : 'abc',
        'password' : 'def'
    }
]

"""