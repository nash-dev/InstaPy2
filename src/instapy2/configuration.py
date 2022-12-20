from .helpers import LocationHelper
from .helpers import PeopleHelper

from .utilities import CommentsUtility
from .utilities import FollowsUtility
from .utilities import InteractionsUtility
from .utilities import LikesUtility
from .utilities import LimitationsUtility
from .utilities import MessageUtility

from instagrapi import Client
from instagrapi.types import Media

from json import load
from os import getcwd, sep
from typing import List

import random

class Configuration:
    def __init__(self, session: Client):
        self.session = session

        self.comments = CommentsUtility(session=session)
        self.follows = FollowsUtility(session=session)
        self.interactions = InteractionsUtility()
        self.likes = LikesUtility(session=session)
        self.limitations = LimitationsUtility(session=session)
        self.media = MediaUtility(configuration=self, session=session)
        self.messages = MessageUtility(session=session)

        self.location = LocationHelper(session=session)
        self.people = PeopleHelper(session=session)

    def from_file(self):
        config_json = load(fp=open(file=f'{getcwd()}{sep}config.json'))
        configuration = config_json['accounts'][self.session.username]['configuration']
        print(config_json)

        if 'comments' in configuration: self.comments.from_json(data=configuration['comments'])
        if 'follows' in configuration: self.follows.from_json(data=configuration['follows'])
        if 'interactions' in configuration: self.interactions.from_json(data=configuration['interactions'])
        if 'likes' in configuration: self.likes.from_json(data=configuration['likes'])
        if 'limitations' in configuration: self.limitations.from_json(data=configuration['limitations'])
        if 'messages' in configuration: self.messages.from_json(data=configuration['messages'])
        if 'people' in configuration: self.people.from_json(data=configuration['people'])


    def set_pexels_api_key(self, key: str):
        self.pexels_api_key = key

    def set_unsplash_api_key(self, key: str):
        self.unsplash_api_key = key


class MediaUtility:
    def __init__(self, configuration: Configuration, session: Client):
        self.configuration = configuration
        self.session = session
        
        self.ignore_to_skip_if_contains = []
        self.required_hashtags = []
        self.to_skip = []

    def ignore(self, hashtags: List[str]): # ignore skip if caption contains any
        self.ignore_to_skip_if_contains = hashtags

    def require(self, hashtags: List[str]): # only like if all in caption
        self.required_hashtags = hashtags

    def skip(self, hashtags: List[str]): # don't like if any in caption, may still unfollow
        self.to_skip = hashtags

    def validated_for_interaction(self, media: Media) -> bool:
        if all(hashtag in media.caption_text for hashtag in self.required_hashtags):
            if any(hashtag in media.caption_text for hashtag in self.to_skip):
                return any(hashtag in media.caption_text for hashtag in self.ignore_to_skip_if_contains) and self.configuration.limitations.within_commenters_range(media=media) and self.configuration.limitations.within_followers_range(user=media.user)
            else:
                return self.configuration.limitations.within_commenters_range(media=media) and self.configuration.limitations.within_followers_range(user=media.user)
        else:
            return False
        

    # helper functions for main script
    def medias_location(self, amount: int, location: int, randomize_media: bool, skip_top: bool) -> List[Media]:
        medias = []
        if skip_top:
            medias += [media for media in self.session.location_medias_recent(location_pk=location, amount=amount) if not any(username in media.user.username if media.user.username is not None else '' for username in self.configuration.people.users_to_skip)]
        else:
            medias += [media for media in self.session.location_medias_top(location_pk=location) if not any(username in media.user.username if media.user.username is not None else '' for username in self.configuration.people.users_to_skip)]
            medias += [media for media in self.session.location_medias_recent(location_pk=location, amount=amount - len(medias)) if not any(username in media.user.username if media.user.username is not None else '' for username in self.configuration.people.users_to_skip)]

        if randomize_media:
            random.shuffle(x=medias)

        limited = medias[:amount]

        print(f'[INFO]: Found {len(limited)} of {amount} valid media with the current configuration.')
        return limited


    def medias_tag(self, amount: int, tag: str, randomize_media: bool, skip_top: bool) -> List[Media]:
        medias = []
        print(len(medias))
        if skip_top:
            id = ''
            while len(medias) < amount:
                chunk, max_id = self.session.hashtag_medias_v1_chunk(name=tag, max_amount=amount, tab_key="recent", max_id=id)

                medias += [media for media in chunk if not any(username in media.user.username if media.user.username is not None else '' for username in self.configuration.people.users_to_skip)]
                print(len(medias))

                id = max_id

            # medias_chunk, end_cursor = [media for media in self.session.hashtag_medias_a1_chunk(name=tag, max_amount=amount) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]
        else:
            medias += [media for media in self.session.hashtag_medias_top(name=tag) if not any(username in media.user.username if media.user.username is not None else '' for username in self.configuration.people.users_to_skip)]

            id = ''
            while len(medias) < amount:
                chunk, max_id = self.session.hashtag_medias_v1_chunk(name=tag, max_amount=amount - len(medias), tab_key="recent", max_id=id)

                medias += [media for media in chunk if not any(username in media.user.username if media.user.username is not None else '' for username in self.configuration.people.users_to_skip)]
                print(len(medias))

                id = max_id

        if randomize_media:
            random.shuffle(x=medias)

        limited = medias[:amount]
        print(len(limited))

        print(f'[INFO]: Found {len(limited)} of {amount} valid media with the current configuration.')
        return limited
    

    def medias_username(self, amount: int, username: str, randomize_media: bool) -> List[Media]:
        try:
            medias = []
            id = ''
            while len(medias) < amount:
                chunk, max_id = self.session.user_medias_paginated(user_id=int(self.session.user_id_from_username(username=username if username is not None else '')), amount=amount, end_cursor=id)

                medias += chunk
                id = max_id

            if randomize_media:
                random.shuffle(x=medias)
            
            return medias[:amount]
        except Exception as error:
            print(f'Failed to get media for user: {username}. {error}.')
            return []