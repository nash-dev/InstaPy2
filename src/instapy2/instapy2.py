from .utilities import Utility
from .types import CommentType, LikeType

class InstaPy2(Utility):
    def comment(self, amount: int, iterable: list[int | str], type: CommentType):
        pass

    def like(self, amount: int, iterable: list[int | str], type: LikeType):
        self.logger.error(message='THIS IS A WIP REWORK. PLEASE USE `MAIN`.')
        exit(0)

        match type:
            case LikeType.HASHTAG:
                for element in iterable:
                    hashtag = str(element)

                    identifiers = self.persistence.all_identifiers(table='medias_likes_hashtag')
                    medias = self.medias.get_medias_for_hashtag(amount=amount, hashtag=hashtag, identifiers_to_skip=identifiers)

                    for media in medias:
                        if not self.is_media_validated_for_interaction(media=media):
                            self.logger.error(message='Media is not validated for interaction.')
                        else:
                            self.logger.info(message='Media is validated for interaction.')
                            if not self.persistence.identifier_exists(table='medias_likes_hashtag', identifier=media.id):
                                try:
                                    liked = self.session.media_like(media_id=media.id)
                                    if liked:
                                        self.persistence.insert_identifier(table='medias_likes_hashtag', identifier=media.id)

                                    if not liked:
                                        self.logger.error(message='Failed to like media.')
                                    else:
                                        self.logger.info(message='Successfully liked media.')
                                except:
                                    self.logger.error(message='Failed to like media.')
            case LikeType.USER:
                for elem in iterable:
                    username = str(elem)

                    identifiers = self.persistence.all_identifiers(table='medias_likes_user')
                    medias = self.medias.get_medias_for_user(amount=amount, username=username, identifiers_to_skip=identifiers)

                    if medias is None:
                        self.logger.error(message=f'An error occurred while scraping media for user: {username}.')
                    else:
                        for media in medias:
                            if not self.is_media_validated_for_interaction(media=media):
                                self.logger.error(message='Media is not validated for interaction.')
                            else:
                                self.logger.info(message='Media is validated for interaction.')
                                if not self.persistence.identifier_exists(table='medias_likes_user', identifier=media.id):
                                    try:
                                        liked = self.session.media_like(media_id=media.id)
                                        if liked:
                                            self.persistence.insert_identifier(table='medias_likes_user', identifier=media.id)

                                        if not liked:
                                            self.logger.error(message='Failed to like media.')
                                        else:
                                            self.logger.info(message='Successfully liked media.')
                                    except:
                                        self.logger.error(message='Failed to like media.')