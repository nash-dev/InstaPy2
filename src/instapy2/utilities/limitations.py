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
        self.skip_public = False
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

    def set_skip_public(self, skip: bool):
        self.skip_public = skip

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
            user_info = self.session.user_info_by_username(username=username) if username is not None else None
            if user_info is not None:
                if self.skip_business and user_info.is_business:
                    return False
                elif self.skip_private and user_info.is_private:
                    return False
                elif self.skip_public and not user_info.is_private:
                    return False
                elif self.skip_verified and user_info.is_verified:
                   return False
                else:
                    return True
            else:
                return False


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