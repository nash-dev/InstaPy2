"""
    multiple_sessions.py shows how to create multiple InstaPy2 sessions.
    This session can then be used to configure and perform actions.

    All actions performed will occur for each account used.

    Note: Use of multiple sessions is only recommended after having used the account once successfully,
    this is because verification_code may cause an issue upon initial login.
"""

from instapy2 import InstaPy2

accounts = [
    {
        'username' : '',
        'password' : ''
    },
    {
        'username' : '',
        'password' : ''
    }
]

session = InstaPy2()
for account in accounts:
    session.login(username='', password='', verification_code='')

    # do stuff