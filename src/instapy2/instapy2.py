from .utilities import Utility
from .types import LikeType

class InstaPy2(Utility):
    def like(self, amount: int, iterable: list[int | str], type: LikeType):
        self.logger.error(message='THIS IS A WIP REWORK. PLEASE USE `MAIN`.')
        exit(0)

        match type:
            case LikeType.HASHTAG:
                for element in iterable:
                    hashtag = str(element)

                    ids = self.persistence.all_identifiers(table='medias')

                    medias = self.medias.get_medias_for_hashtag(amount=amount, hashtag=hashtag, identifiers_to_skip=ids)
                    for media in medias:
                        if not self.is_media_validated_for_interaction(media=media):
                            self.logger.error(message='Media is not validated for interaction.')
                        else:
                            self.logger.info(message='Media is validated for interaction.')
                            if not self.persistence.identifier_exists(table='medias', identifier=media.id):
                                try:
                                    liked = self.session.media_like(media_id=media.id)
                                    if liked:
                                        self.logger.info('>>> Identifier to be inserted here')
                                        # insert_id(name='medias', identifier=media.id)

                                    if not liked:
                                        self.logger.error(message='Failed to like media.')
                                    else:
                                        self.logger.info(message='Successfully liked media.')
                                except:
                                    self.logger.error(message='Failed to like media.')