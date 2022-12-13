from instagrapi import Client
from instagrapi.types import UserShort

from typing import List, Tuple

class MessageUtility:
    def __init__(self, session: Client):
        self.session = session

        self.enabled = False
        self.follower_range = 1, 10000
        self.messages = []
        self.percentage = 0

    def set_enabled(self, enabled: bool):
        """
            Enables the ability to direct message a user.
            
            :param enabled: enabled=True means a user will be direct messaged.
        """
        self.enabled = enabled

    def set_follower_range(self, follower_range: Tuple[int, int]):
        """
            Sets the limit to how many followers a user can have to be direct messaged.

            :param follower_range: follower_range=(1, 100) means a user with between 1 and 100
            followers will be direct messaged.
        """
        self.follower_range = follower_range

    def set_messages(self, messages: List[str]):
        """
            Sets the messages to be used when direct messaging a user.

            :param messages: messages=['message 1', ' message 2', 'message 3 @{}']
            
            Adding @{} will tag the other user in the direct message.
        """
        self.messages = messages

    def set_percentage(self, percentage: int):
        """
            Set the percentage of users to direct message.

            :param percentage: percentage=25 means every 4th user will be direct messaged.
        """
        self.percentage = percentage

    def message(self, user: UserShort, text: str) -> Tuple[Exception, bool]:
        try:
            messaged = self.session.direct_send(text=text.format(user.username), user_ids=[self.session.user_id_from_username(username=user.username)])
            return (None, messaged is not None)
        except Exception as error:
            return error, False