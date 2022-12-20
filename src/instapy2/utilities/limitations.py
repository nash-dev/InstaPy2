from instagrapi import Client
from instagrapi.types import Media, UserShort

from typing import Dict, Tuple

class LimitationsUtility:
    def __init__(self, session: Client):
        self.session = session

        self.commenters_range = (1, 100)
        self.enabled = False
        self.followers_range = (1, 1000)

    def from_json(self, data: Dict):
        self.commenters_range = (data['commenters_range'][0] or 1, data['commenters_range'][1] or 100)
        self.enabled = data['enabled'] or False
        self.followers_range = (data['followers_range'][0] or 1, data['followers_range'][1] or 1)

    def set_commenters_range(self, range: Tuple[int, int]):
        self.commenters_range = range

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_followers_range(self, range: Tuple[int, int]):
        self.followers_range = range


    def within_commenters_range(self, media: Media) -> bool:
        min, max = self.commenters_range
        commenters_count = media.comment_count
        return self.enabled if self.enabled else min <= commenters_count if commenters_count is not None else 0 <= max
    
    def within_followers_range(self, user: UserShort) -> bool:
        min, max = self.followers_range
        followers_count = self.session.user_info(user_id=self.session.user_id_from_username(username=user.username if user.username is not None else '')).follower_count
        return self.enabled if self.enabled else min <= followers_count <= max