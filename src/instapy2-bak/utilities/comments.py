from emoji import emojize
from instagrapi import Client
from instagrapi.types import Media

from typing import Dict, List, Tuple, Union

class CommentsUtility:
    def __init__(self, session: Client):
        self.session = session

        self.comments = []
        self.enabled = False
        self.percentage = 0

    def from_json(self, data: Dict):
        self.comments = data['comments'] or []
        self.enabled = data['enabled'] or False
        self.percentage = data['percentage'] or 0


    def set_comments(self, comments: List[str]):
        self.comments = comments

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_percentage(self, percentage: int):
        self.percentage = percentage


    def comment(self, media: Media, text: str) -> Tuple[Union[Exception, None], bool]:
        try:
            commented = self.session.media_comment(media_id=media.id, text=emojize(string=text).format(media.user.username))
            return (None, commented is not None)
        except Exception as error:
            return (error, False)