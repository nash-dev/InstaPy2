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
        self.comments = CommentsUtility(session=session)
        self.follows = FollowsUtility(session=session)
        self.interactions = InteractionsUtility(session=session)
        self.likes = LikesUtility(session=session)
        self.media = MediaUtility(session=session)
        self.messages = MessageUtility(session=session)

        self.location = LocationHelper(session=session)
        self.people = PeopleHelper(session=session)