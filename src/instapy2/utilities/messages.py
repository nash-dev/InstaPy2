from instagrapi import Client
from instagrapi.types import UserShort

from typing import Dict, List, Tuple, Union

class MessageUtility:
    def __init__(self, session: Client):
        self.session = session

        self.enabled = False
        self.messages = []
        self.percentage = 0

    def from_json(self, data: Dict):
        self.enabled = data['enabled'] or False
        self.messages = data['messages'] or []
        self.percentage = data['percentage'] or 0

    def set_enabled(self, enabled: bool):
        """
            Enables the ability to direct message a user.
            
            :param enabled: enabled=True means a user will be direct messaged.
        """
        self.enabled = enabled

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

    def message(self, user: Union[str, UserShort], text: str) -> Tuple[Union[Exception, None], bool]:
        try:
            if isinstance(user, str):
                messaged = self.session.direct_send(text=text.format(user), user_ids=[int(self.session.user_id_from_username(username=user))])
            else:
                messaged = self.session.direct_send(text=text.format(user.username), user_ids=[int(self.session.user_id_from_username(username=user.username if user.username is not None else ''))])
            return (None, messaged is not None)
        except Exception as error:
            return error, False