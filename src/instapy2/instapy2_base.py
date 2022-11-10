from .configuration import Configuration

from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice
from instagrapi.types import Media

from typing import List, Tuple

import email, imaplib, random, re, os

class InstaPy2Base:
    def __init__(self, delay_range: Tuple[float, float] = None):
        if delay_range is not None:
            min, max = delay_range
        else:
            min, max = (1, 5)

        self.session = Client(delay_range=[min, max])

    def login(self, username: str = None, password: str = None, verification_code: str = None):
        if username is None:
            print('[ERROR]: Username has not been set.')
            return

        if password is None:
            print('[ERROR]: Password has not been set.')
            return

        if os.path.exists(path=os.getcwd() + f'{os.path.sep}files{os.path.sep}settings.json'):
            self.session.load_settings(path=os.getcwd() + f'{os.path.sep}files{os.path.sep}settings.json')
            logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
        else:
            logged_in = self.session.login(username=username, password=password, verification_code=verification_code)
            self.session.dump_settings(path=os.getcwd() + f'{os.path.sep}files{os.path.sep}settings.json')

        print(f'[INFO]: Successfully logged in as: {self.session.username}.' if logged_in else f'[ERROR]: Failed to log in.')
        self.configuration = Configuration(session=self.session)

    def __get_code_from_email(self, username):
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(self.email, self.password)
        mail.select("inbox")
        result, data = mail.search(None, "(UNSEEN)")
        assert result == "OK", "Error1 during get_code_from_email: %s" % result

        ids = data.pop().split()
        for num in reversed(ids):
            mail.store(num, "+FLAGS", "\\Seen")  # mark as read
            result, data = mail.fetch(num, "(RFC822)")
            assert result == "OK", "Error2 during get_code_from_email: %s" % result

            msg = email.message_from_string(data[0][1].decode())
            payloads = msg.get_payload()
            if not isinstance(payloads, list):
                payloads = [msg]
            code = None

            for payload in payloads:
                body = payload.get_payload(decode=True).decode()
                if "<div" not in body:
                    continue

                match = re.search(">([^>]*?({u})[^<]*?)<".format(u=username), body)
                if not match:
                    continue

                print("Match from email:", match.group(1))
                match = re.search(r">(\d{6})<", body)
                if not match:
                    print('Skip this email, "code" not found')
                    continue

                code = match.group(1)
                if code:
                    return code
        return False

    def __challenge_code_handler(self, username, choice):
        if choice is ChallengeChoice.SMS:
            return False
        else:
            return self.__get_code_from_email(username)


    def twofa(self, email: str = None, password: str = None):
        self.email = email
        self.password = password
        self.session.challenge_code_handler = self.__challenge_code_handler

    def __medias_location(self, amount: int, location: int, randomize_media: bool, skip_top: bool) -> List[Media]:
        medias = []
        if skip_top:
            medias += [media for media in self.session.location_medias_recent(location_pk=location, amount=amount) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]
        else:
            medias += [media for media in self.session.location_medias_top(location_pk=location) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]
            medias += [media for media in self.session.location_medias_recent(location_pk=location, amount=amount - len(medias)) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]

        if randomize_media:
            random.shuffle(x=medias)

        limited = medias[:amount]

        print(f'[INFO]: Found {len(limited)} of {amount} valid media with the current configuration.')
        return limited

    def __medias_tag(self, amount: int, tag: str, randomize_media: bool, skip_top: bool) -> List[Media]:
        medias = []
        if skip_top:
            medias += [media for media in self.session.hashtag_medias_recent(name=tag, amount=amount) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]
        else:
            medias += [media for media in self.session.hashtag_medias_top(name=tag) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]
            medias += [media for media in self.session.hashtag_medias_recent(name=tag, amount=amount - len(medias)) if not any(username in media.user.username for username in self.configuration.people.users_to_skip)]

        if randomize_media:
            random.shuffle(x=medias)

        limited = medias[:amount]

        print(f'[INFO]: Found {len(limited)} of {amount} valid media with the current configuration.')
        return limited
    
    def __medias_username(self, amount: int, username: str, randomize_media: bool) -> List[Media]:
        try:
            medias = self.session.user_medias(user_id=self.session.user_id_from_username(username=username), amount=amount)
            
            if randomize_media:
                random.shuffle(x=medias)
            
            return medias[:amount]
        except Exception as error:
            print(f'Failed to get media for user: {username}. {error}.')
            return []