from instapy2 import InstaPy2
from instapy2.types import LikeType

session = InstaPy2()
session.login(username='', password='')

session.like(amount=10, iterable=['christmas'], type=LikeType.Tags)