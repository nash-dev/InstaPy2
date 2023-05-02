from .authentication import Authentication

from instagrapi.types import Media

class Utility(Authentication):
    def get_pk(self, query: str) -> int | None:
        places = self.session.fbsearch_places(query=query)
        place_tuple = [(place.name, place.city, place.zip, place.pk) for place in places]

        for index, place in enumerate(iterable=place_tuple):
            name, city, zip, pk = place
            selection_string = ''
            if name is not None and name != '':
                selection_string += name
            if city is not None and city != '':
                selection_string += f', {city}'
            if zip is not None and zip != '':
                selection_string += f', {zip}'
            self.logger.info(message=f'[INFO]: {index + 1}: {selection_string}')


        selection = int(input(f'Enter the index for the correct location (1-{len(place_tuple)}): '))
        if 1 <= selection <= len(places):
            _, _, _, pk = place_tuple[selection - 1]
            return pk
        else:
            self.logger.error(message=f'[ERROR]: Selection is invalid. Please choose between 1-{len(places)}.')
            return None
        

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

    def do_after(self, function):
        function()

    def nop(self):
        pass