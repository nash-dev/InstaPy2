from instagrapi import Client
from instagrapi.types import Media

class Limitations:
    def __init__(self, session: Client):
        self.session = session

        self.commenter_range = (1, 1000)
        self.enabled = False
        self.follower_range = (1, 1000)
        self.following_range = (1, 1000)

        self.skip_business = False
        self.skip_private = True
        self.skip_verified = False


    def set_commenter_range(self, range: tuple[int, int]):
        self.commenter_range = range

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_follower_range(self, range: tuple[int, int]):
        self.follower_range = range

    def set_skip_business(self, skip: bool):
        self.skip_business = skip

    def set_skip_private(self, skip: bool):
        self.skip_private = skip

    def set_skip_verified(self, skip: bool):
        self.skip_verified = skip


    def is_account_appropriate(self, media: Media) -> bool:
        enabled = self.enabled
        username = media.user.username

        if not enabled:
            return True
        else:
            if username is None:
                return False
            else:
                try:
                    user_info = self.session.user_info_by_username(username=username)
                except:
                    user_info = None
                
                return False if user_info is None else all([self.skip_business and not user_info.is_business, self.skip_private and not user_info.is_private, self.skip_verified and not user_info.is_verified])

    def within_commenter_range(self, media: Media) -> bool:
        enabled = self.enabled
        min, max = self.commenter_range
        
        commenter_count = media.comment_count or 0
        return True if not enabled else min <= commenter_count <= max

    def within_follower_range(self, media: Media) -> bool:
        enabled = self.enabled
        min, max = self.follower_range
        username = media.user.username

        try:
            follower_count = self.session.user_info_by_username(username=username).follower_count if username is not None else 0
        except:
            follower_count = 0
        
        return True if not enabled else min <= follower_count <= max
    
    def within_following_range(self, media: Media) -> bool:
        enabled = self.enabled
        min, max = self.following_range
        username = media.user.username

        try:
            following_count = self.session.user_info_by_username(username=username).following_count if username is not None else 0
        except:
            following_count = 0
        
        return True if not enabled else min <= following_count <= max