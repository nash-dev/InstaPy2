from .configuration import Configuration

from instagrapi import Client
from instagrapi.types import Media

from typing import List

import random, os

class InstaPy2Base:
    def login(self, username: str = None, password: str = None, verification_code: str = ''):
        self.session = Client()
        if os.path.exists(path=os.getcwd() + f'{os.path.sep}files{os.path.sep}settings.json'):
            self.session.load_settings(path=os.getcwd() + f'{os.path.sep}files{os.path.sep}settings.json')
            logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
        else:
            logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
            self.session.dump_settings(path=os.getcwd() + f'{os.path.sep}files{os.path.sep}settings.json')

        print(f'[INFO]: Successfully logged in as: {self.session.username}.' if logged_in else f'[ERROR]: Failed to log in.')
        self.configuration = Configuration(session=self.session)


    def __medias_location(self, amount: int, location: int, randomize_media: bool, skip_top: bool) -> List[Media]:
        medias = []
        if skip_top:
            medias += [media for media in self.session.location_medias_recent(location_pk=location, amount=amount) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]
        else:
            medias += [media for media in self.session.location_medias_top(location_pk=location) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]
            medias += [media for media in self.session.location_medias_recent(location_pk=location, amount=amount - len(medias)) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]

        if randomize_media:
            random.shuffle(x=medias)

        limited = medias[:amount]

        print(f'[INFO]: Found {len(limited)} of {amount} valid media with the current configuration.')
        return limited


    def __medias_tag(self, amount: int, tag: str, randomize_media: bool, skip_top: bool) -> List[Media]:
        medias = []
        if skip_top:
            medias += [media for media in self.session.hashtag_medias_recent(name=tag, amount=amount) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]
        else:
            medias += [media for media in self.session.hashtag_medias_top(name=tag) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]
            medias += [media for media in self.session.hashtag_medias_recent(name=tag, amount=amount - len(medias)) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]

        if randomize_media:
            random.shuffle(x=medias)

        limited = medias[:amount]

        print(f'[INFO]: Found {len(limited)} of {amount} valid media with the current configuration.')
        return limited
    

    def __medias_username(self, amount: int, username: str, randomize_media: bool) -> List[Media]:
        try:
            medias = self.session.user_medias(user_id=self.session.user_id_from_username(username=username), amount=amount)
            
            if randomize_media:
                random.shuffle(x=medias)
            
            return medias[:amount]
        except Exception as error:
            print(f'Failed to get media for user: {username}. {error}.')
            return []