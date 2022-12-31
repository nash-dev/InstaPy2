from ..utilities import Limitations

from logging import basicConfig, DEBUG, error, info
from os import getcwd, mkdir, sep
from os.path import exists
from pathlib import Path

from instagrapi import Client

class Authentication:
    def __files_exists(self, path: str) -> bool:
        return exists(path=path)
    
    def __make_files(self, path: str) -> bool:
        return mkdir(path=path) is not None

    def __settings_exists(self, path: str) -> bool:
        return exists(path=path)
    

    def login(self, username: str, password: str, verification_code: str = '', proxy: str = ''):
        files_path = getcwd() + sep + 'files'
        if not self.__files_exists(path=files_path):
            _ = self.__make_files(path=files_path)

        self.session = Client(proxy=proxy)
        settings_path = files_path + sep + username + '.json'
        try:
            if not self.__settings_exists(path=settings_path):
                logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
                self.session.dump_settings(path=Path(settings_path))
            else:
                self.session.load_settings(path=Path(settings_path))
                logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
        except:
            error(msg='There was an error while logging in.')
            exit(0)

        basicConfig(format='[%(levelname)s]: %(message)s', level=DEBUG)
        error(msg='Failed to log in successfully.') if not logged_in else info(msg=f'Successfully logged in as: {self.session.username}.')

        # MARK: Placing them here to lessen the amount of code needed to configure shit.
        self.limitations = Limitations(session=self.session)