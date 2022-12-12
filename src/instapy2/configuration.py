from .helpers import LocationHelper
from .helpers import PeopleHelper

from .utilities import CommentsUtility
from .utilities import FollowsUtility
from .utilities import InteractionsUtility
from .utilities import LikesUtility
from .utilities import MediaUtility
from .utilities import MessageUtility

from instagrapi import Client

class Configuration:
    def __init__(self, session: Client):
        self.comments = CommentsUtility(configuration=self, session=session)
        self.follows = FollowsUtility(configuration=self, session=session)
        self.interactions = InteractionsUtility(configuration=self, session=session)
        self.likes = LikesUtility(configuration=self, session=session)
        self.media = MediaUtility(configuration=self, session=session)
        self.messages = MessageUtility(configuration=self, session=session)

        self.location = LocationHelper(session=session)
        self.people = PeopleHelper(session=session)

    def set_pexels_api_key(self, key: str):
        self.pexels_api_key = key

    def set_unsplash_api_key(self, key: str):
        self.unsplash_api_key = key