from instagrapi import Client
from instagrapi.types import Media

class Limitations:
    def __init__(self, session: Client):
        self.session = session

        self.enabled = False
        self.follower_range = (1, 1000)

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_follower_range(self, range: tuple[int, int]):
        self.follower_range = range

    
    def within_follower_range(self, media: Media):
        enabled = self.enabled
        min, max = self.follower_range
        username = media.user.username

        follower_count = self.session.user_info_by_username(username=username).follower_count if username is not None else 0
        return enabled if enabled else min <= follower_count <= max