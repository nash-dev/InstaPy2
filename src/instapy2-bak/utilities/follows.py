from instagrapi import Client
from instagrapi.types import UserShort

from typing import Dict, Tuple, Union

class FollowsUtility:
    def __init__(self, session: Client):
        self.session = session

        self.enabled = False
        self.percentage = 0

    def from_json(self, data: Dict):
        self.enabled = data['enabled'] or False
        self.percentage = data['percentage'] or 0


    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_percentage(self, percentage: int):
        self.percentage = percentage


    def follow(self, user: Union[int, UserShort]) -> Tuple[Union[Exception, None], bool]:
        try:
            followed = self.session.user_follow(user_id=self.session.user_id_from_username(username=user.username if user.username is not None else '') if isinstance(user, UserShort) else f'{user}')
            return (None, followed)
        except Exception as error:
            return (error, False)
        
"""
    def unfollow(self, user_id: str, username: str) -> Tuple[Union[Exception, None], bool]:
        try:
            unfollowed = self.session.user_unfollow(user_id=user_id)
            return None, unfollowed
        except Exception as error:
            return (error, False)
"""