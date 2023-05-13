from instapy2 import InstaPy2
from instapy2.types import LikeType

session = InstaPy2()
session.login(username='', password='')

session.configuration.comments.set_enabled(enabled=True)
session.configuration.comments.set_percentage(percentage=75)
session.configuration.comments.set_com61ments(comments=[
    'Yes i am the english comment you been looking for',
    'Good stuff',
    'Im here to comment @{}'
])

session.like(amount=10, iterable=['fashion'], type=LikeType.Tags)