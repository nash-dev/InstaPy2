from .helpers.location import LocationHelper
from .helpers.people import PeopleHelper

from .utilities.comments import CommentsUtility
from .utilities.follows import FollowsUtility
from .utilities.interactions import InteractionsUtility
from .utilities.likes import LikesUtility
from .utilities.media import MediaUtility


from instagrapi import Client

class Configuration:
    def __init__(self, session: Client):
        # utilities
        self.comments = CommentsUtility(session=session)
        self.follows = FollowsUtility(session=session)
        self.interactions = InteractionsUtility(session=session)
        self.likes = LikesUtility(session=session)
        self.media = MediaUtility(session=session)

        # helpers
        self.location = LocationHelper(session=session)
        self.people = PeopleHelper(session=session)