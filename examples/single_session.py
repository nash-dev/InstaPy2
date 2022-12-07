"""
    single_session.py shows how to create a single InstaPy2 session.
    This session can then be used to configure and perform actions.

    All actions performed will only occur from the one account used.
"""

from instapy2 import InstaPy2

session = InstaPy2()
session.login(username='', password='', verification_code='')

# do stuff