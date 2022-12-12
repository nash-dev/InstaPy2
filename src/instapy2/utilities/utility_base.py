from ..configuration import Configuration

from instagrapi import Client

class UtilityBase:
    def __init__(self, configuration: Configuration, session: Client):
        self.configuration = configuration
        self.session = session