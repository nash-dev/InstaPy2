from .instapy2_base import InstaPy2Base

from .types import CommentType
from .types import FollowType
from .types import LikeType
from .types import PostType
from .types import UnfollowType

from typing import List, Union

import random

class InstaPy2(InstaPy2Base):
    def comment(self, amount: int = 50, iterable: List[Union[int, str]] = [], type: CommentType = None, **kwargs):
        randomize_media = kwargs['randomize_media'] if 'randomize_media' in kwargs.keys() else False
        skip_top = kwargs['skip_top'] if 'skip_top' in kwargs.keys() else True

        match type:
            case CommentType.Locations:
                for location in iterable:
                    medias = self.configuration.media.medias_location(amount=amount, location=location, randomize_media=randomize_media, skip_top=skip_top)

                    for media in medias:
                        if self.configuration.media.validated_for_interaction(media=media):
                            commenting = random.randint(a=0, b=100) <= self.configuration.comments.percentage
                            following = random.randint(a=0, b=100) <= self.configuration.follows.percentage

                            if self.configuration.comments.enabled and commenting:
                                _, _ = self.configuration.comments.comment(media=media, text=random.choice(seq=self.configuration.comments.comments))

                            if self.configuration.follows.enabled and following:
                                self.follow(iterable=media.user.username, type=FollowType.Users)
            case _:
                print('[ERROR]: No `type` was provided.')


    def follow(self, amount: int = 50, iterable: List[Union[int, str]] = [], type: FollowType = None, **kwargs):
        randomize_media = kwargs['randomize_media'] if 'randomize_media' in kwargs.keys() else False
        randomize_tags = kwargs['randomize_tags'] if 'randomize_tags' in kwargs.keys() else False
        skip_top = kwargs['skip_top'] if 'skip_top' in kwargs.keys() else True

        if not isinstance(iterable, list):
            iterable = [iterable]

        match type:
            case FollowType.Commenters:
                for username in iterable:
                    medias = self.configuration.media.medias_username(amount=amount, username=username, randomize_media=randomize_media)

                    usernames = []
                    found_amount = False
                    for media in medias:
                        if self.configuration.media.validated_for_interaction(media=media):
                            if found_amount:
                                break

                            for comment in self.session.media_comments(media_id=media.id):
                                if comment.user.username not in usernames and comment.user.username != self.session.username and len(usernames) < amount:
                                    usernames.append(comment.user.username)
                                else:
                                    found_amount = True
                                    break
                        else:
                            pass

                    self.follow(amount=amount, iterable=usernames, type=FollowType.Users)
            case FollowType.Likers:
                medias = self.configuration.media.medias_username(amount=amount, username=self.session.username, randomize_media=randomize_media)

                usernames = []
                found_amount = False
                for media in medias:
                    if self.configuration.media.validated_for_interaction(media=media):
                        if found_amount:
                            break

                        for liker in self.session.media_likers(media_id=media.id):
                            if liker.username not in usernames and len(usernames) < amount:
                                usernames.append(liker.username)
                            else:
                                found_amount = True
                                break
                    else:
                        pass

                self.follow(amount=amount, iterable=usernames, type=FollowType.Users)
            case FollowType.Locations:
                for location in iterable:
                    medias = self.configuration.media.medias_location(amount=amount, location=location, randomize_media=randomize_media, skip_top=skip_top)

                    usernames = []
                    found_amount = False
                    for media in medias:
                        if self.configuration.media.validated_for_interaction(media=media):
                            if found_amount:
                                break

                            if media.user.username not in usernames and media.user.username != self.session.username and len(usernames) < amount:
                                usernames.append(media.user.username)
                            else:
                                found_amount = True
                                break
                        else:
                            pass
                        
                    self.follow(amount=amount, iterable=usernames, type=FollowType.Users)
            case FollowType.Tags:
                tags = [tag.strip() for tag in iterable]

                if randomize_tags:
                    random.shuffle(x=tags)

                usernames = []
                found_amount = False
                for tag in tags:
                    medias = self.configuration.media.medias_tag(amount=amount, tag=tag, randomize_media=randomize_media)

                    for media in medias:
                        if self.configuration.media.validated_for_interaction(media=media):
                            if found_amount:
                                break

                            """random.randint(a=0, b=100) <= self.configuration.follows.percentage and"""
                            if media.user.username not in usernames and len(usernames) < amount:
                                usernames.append(media.user.username)
                            else:
                                found_amount = True
                                break
                        else:
                            pass

                self.follow(amount=amount, iterable=usernames, type=FollowType.Users)
            case FollowType.Users:
                followed_count = 0

                for username in iterable:
                    user_id = self.session.user_id_from_username(username=username)
                    following = self.session.user_friendship_v1(user_id=user_id).following
                    messaging = random.randint(a=0, b=100) <= self.configuration.messages.percentage

                    did_follow = False
                    if not following:
                        _, did_follow = self.configuration.follows.follow(user=user_id)

                    if self.configuration.messages.enabled and messaging:
                        _, _ = self.configuration.messages.message(user=media.user, text=random.choice(seq=self.configuration.messages.messages))

                    if did_follow:
                        followed_count += 1

                    interacting = random.randint(a=0, b=100) <= self.configuration.interactions.percentage
                    if did_follow and self.configuration.interactions.enabled and interacting:
                        self.interact_users(amount=self.configuration.interactions.amount, usernames=username, randomize_media=self.configuration.interactions.randomize)

                print(f'[INFO]: Followed {followed_count} of {len(iterable)} users.')
            case _:
                print('[ERROR]: No `type` was provided.')
    
        
    def like(self, amount: int = 50, iterable: List[Union[int, str]] = [], type: LikeType = None, **kwargs):
        """
            Possible **kwargs
                randomize_likes, randomize_media, randomize_tags, skip_top
        """

        randomize_likes = kwargs['randomize_likes'] if 'randomize_likes' in kwargs.keys() else False
        randomize_media = kwargs['randomize_media'] if 'randomize_media' in kwargs.keys() else False
        randomize_tags = kwargs['randomize_tags'] if 'randomize_tags' in kwargs.keys() else False
        skip_top = kwargs['skip_top'] if 'skip_top' in kwargs.keys() else True

        match type:
            case LikeType.Feed:
                if not isinstance(iterable, list):
                    iterable = [iterable]

                for username in iterable:
                    medias = self.configuration.media.medias_username(amount=amount, username=username)

                    for media in medias:
                        if randomize_likes and random.choice([True, False]):
                            pass
                        else:
                            if self.configuration.media.validated_for_interaction(media=media):
                                liked = self.configuration.likes.like(media=media)

                                if self.configuration.comments.enabled_for_liked_media or liked:
                                    commenting = random.randint(a=0, b=100) <= self.configuration.comments.percentage
                                    following = random.randint(a=0, b=100) <= self.configuration.follows.percentage

                                    if self.configuration.comments.enabled and commenting:
                                        _, _ = self.configuration.comments.comment(media=media, text=random.choice(seq=self.configuration.comments.comments))

                                    did_follow = False
                                    if self.configuration.follows.enabled and following:
                                        _, did_follow = self.configuration.follows.follow(user=media.user)

                                    interacting = random.randint(a=0, b=100) <= self.configuration.interactions.percentage
                                    if did_follow and self.configuration.interactions.enabled and interacting:
                                        self.interact_users(amount=self.configuration.interactions.amount, usernames=media.user.username, randomize_media=self.configuration.interactions.randomize)

            case LikeType.Locations:
                for location in iterable:
                    medias = self.configuration.media.medias_location(amount=amount, location=location, randomize_media=randomize_media, skip_top=skip_top)

                    for media in medias:
                        if self.configuration.media.validated_for_interaction(media=media):
                            liked = self.configuration.likes.like(media=media)

                            if self.configuration.comments.enabled_for_liked_media or liked:
                                commenting = random.randint(a=0, b=100) <= self.configuration.comments.percentage
                                following = random.randint(a=0, b=100) <= self.configuration.follows.percentage

                                if self.configuration.comments.enabled and commenting:
                                    _, _ = self.configuration.comments.comment(media=media, text=random.choice(seq=self.configuration.comments.comments))

                                if self.configuration.follows.enabled and following:
                                    _, _ = self.configuration.follows.follow(user=media.user)
            case LikeType.Tags:
                tags = [tag.strip() for tag in iterable]

                if randomize_tags:
                    random.shuffle(x=tags)

                for tag in tags:
                    medias = self.configuration.media.medias_tag(amount=amount, tag=tag, randomize_media=randomize_media, skip_top=skip_top)

                    for media in medias:
                        if self.configuration.media.validated_for_interaction(media=media):
                            liked = self.configuration.likes.like(media=media)

                            if self.configuration.comments.enabled_for_liked_media or liked:
                                commenting = random.randint(a=0, b=100) <= self.configuration.comments.percentage
                                following = random.randint(a=0, b=100) <= self.configuration.follows.percentage

                                if self.configuration.comments.enabled and commenting:
                                    _, _ = self.configuration.comments.comment(media=media, text=random.choice(seq=self.configuration.comments.comments))

                                did_follow = False
                                if self.configuration.follows.enabled and following:
                                    _, did_follow = self.configuration.follows.follow(user=media.user)

                                interacting = random.randint(a=0, b=100) <= self.configuration.interactions.percentage
                                if did_follow and self.configuration.interactions.enabled and interacting:
                                    self.interact_users(amount=self.configuration.interactions.amount, usernames=media.user.username, randomize_media=self.configuration.interactions.randomize)
            case LikeType.Users:
                if not isinstance(iterable, list):
                    iterable = [iterable]

                for username in iterable:
                    medias = self.configuration.media.medias_username(amount=amount, username=username, randomize_media=randomize_media)

                    for media in medias:
                        if self.configuration.media.validated_for_interaction(media=media):
                            liked = self.configuration.likes.like(media=media)

                            if self.configuration.comments.enabled_for_liked_media or liked:
                                commenting = random.randint(a=0, b=100) <= self.configuration.comments.percentage
                                following = random.randint(a=0, b=100) <= self.configuration.follows.percentage
                                messaging = random.randint(a=0, b=100) <= self.configuration.messages.percentage

                                if self.configuration.comments.enabled and commenting:
                                    _, _ = self.configuration.comments.comment(media=media, text=random.choice(seq=self.configuration.comments.comments))

                                if self.configuration.follows.enabled and following:
                                    _, _ = self.configuration.follows.follow(user=media.user)

                                if self.configuration.messages.enabled and messaging:
                                    _, _ = self.configuration.messages.message(user=media.user, text=random.choice(seq=self.configuration.messages.messages))
            case _:
                print('[ERROR]: No `type` was provided.')


    def unfollow(self, amount: int = 10, iterable: List[str] = [], type: UnfollowType = None, **kwargs):
        total_unfollowed = 0

        randomize_usernames = kwargs['randomize_usernames'] if 'randomize_usernames' in kwargs.keys() else False
        only_nonfollowers = kwargs['only_nonfollowers'] if 'only_nonfollowers' in kwargs.keys() else False

        match type:
            case UnfollowType.Users:
                user_ids = []
                if len(iterable) == 0:
                    [user_ids.append(user_id) for user_id in self.session.user_following(user_id=self.session.user_id, amount=amount).keys() if self.session.username_from_user_id(user_id=user_id) not in self.configuration.people.friends_to_skip]
                else:
                    [user_ids.append(self.session.user_id_from_username(username=username)) for username in iterable]

                if randomize_usernames:
                    random.shuffle(x=user_ids)

                for user_id in user_ids:
                    if only_nonfollowers and not self.session.user_friendship_v1(user_id=user_id).followed_by:
                        _, unfollowed = self.configuration.follows.unfollow(user_id=user_id)
                        if unfollowed:
                            total_unfollowed += 1
            case _:
                print('[ERROR]: No `type` was provided.')
        
        print(f'[INFO]: Unfollowed {total_unfollowed} of {len(user_ids)} users.')


    def interact_users(self, amount: int = 10, usernames: List[str] = [], randomize_media: bool = False):
        if not isinstance(usernames, list):
            usernames = [usernames]

        commented_count = 0
        followed_count = 0
        liked_count = 0


        for index, username in enumerate(iterable=usernames):
            print(f'[INFO]: Username [{index + 1}/{len(usernames)}]')
            print(f'[INFO]: {username}')

            if username not in self.configuration.people.friends_to_skip:
                medias = self.configuration.media.medias_username(amount=amount, username=username, randomize_media=randomize_media)

                following = random.randint(0, 100) <= self.configuration.follows.percentage

                for index, media in enumerate(iterable=medias):
                    if self.configuration.media.validated_for_interaction(media=media):
                        if index > 0:
                            liking = random.randint(a=0, b=100) <= self.configuration.likes.percentage
                            commenting = random.randint(a=0, b=100) <= self.configuration.comments.percentage

                            if self.configuration.likes.enabled and liking:
                                liked = self.configuration.likes.like(media=media)
                                if liked:
                                    liked_count += 1

                                if commenting and liked or self.configuration.comments.enabled_for_liked_media:
                                    try:
                                        commented = self.session.media_comment(media_id=media.id, text=random.choice(seq=self.configuration.comments.comments).format(media.user.username))
                                        print(f'[INFO]: Successfully commented on media: {media.code}' if commented is not None else '[ERROR]: Failed to comment on media.')
                                        if commented:
                                            commented_count += 1
                                    except Exception as error:
                                        print(f'[ERROR]: {error}.')

                if following: # what is dont_follow_inap_post?
                    followed = self.configuration.follows.follow(user_id=self.session.user_id_from_username(username=username))
                    if followed:
                        followed_count += 1

        print(f'[INFO]: Commented on {commented_count} media.')
        print(f'[INFO]: Followed {followed_count} users.')
        print(f'[INFO]: Liked {liked_count} media.')


    def post(self, type: PostType = None, **kwargs):
        match type:
            case PostType.Path:
                path = kwargs['path'] if 'path' in kwargs.keys() else None
                caption = kwargs['caption'] if 'caption' in kwargs.keys() else None
                usertags = kwargs['usertags'] if 'usertags' in kwargs.keys() else []

                if path is not None and caption is not None:
                    self.session.photo_upload(path=path, caption=caption, usertags=usertags)
            case PostType.Pexels:
                print('[INFO]: Pexels is not currently supported.')
            case PostType.Unsplash:
                print('[INFO]: Unsplash is not currently supported.')
            case _:
                print('[ERROR]: No `type` was provided.')