from .authentication import Authentication

from instagrapi.types import Media

class Utility(Authentication):
    def is_media_validated_for_interaction(self, media: Media) -> bool:
        if not self.limitations.within_commenter_range(media=media):
            self.logger.error(message='Post comment count is not within the set commenter range. Skipping.')
            return False
        else:
            if not self.limitations.within_follower_range(media=media):
                self.logger.error(message='Post author\'s follower count is not within the set follower range. Skipping.')
                return False
            else:
                if not self.limitations.within_following_range(media=media):
                    self.logger.error(message='Post author\'s following count is not within the set following range. Skipping.')
                    return False
                else:
                    if not self.limitations.is_account_appropriate(media=media):
                        self.logger.error(message='Post author\'s account is not appropriate with the current configuration. Skipping.')
                        return False
                    else:
                        return True