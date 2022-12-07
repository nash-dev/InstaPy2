from instapy2 import InstaPy2
from instapy2.types import LikeType

session = InstaPy2()
session.login(username='', password='')

session.configuration.comments.set_enabled(enabled=True)
session.configuration.comments.set_percentage(percentage=75)
session.configuration.comments.set_comments(comments=[
    'This is a comment',
    'This is another comment',
    'This is a comment that will tag the author of the post @{}'
])

session.like(amount=10, iterable=['christmas'], type=LikeType.Tags)