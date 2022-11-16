# -*- coding: utf-8 -*-
"""
Post new articles on Mastodon
"""

import string

import logging
logger = logging.getLogger(__name__)

from pelican import signals

# https://github.com/halcy/Mastodon.py

# Copied from Mastodon.py readme - fix it!!
# Register your app! This only needs to be done once. Uncomment the code and substitute in your information.

from mastodon import Mastodon

'''
Mastodon.create_app(
     'pytooterapp',
     api_base_url = 'https://mastodon.social',
     to_file = 'pytooter_clientcred.secret'
)
'''

# Then login. This can be done every time, or use persisted.

from mastodon import Mastodon

mastodon = Mastodon(client_id = 'pytooter_clientcred.secret')
mastodon.log_in(
    'my_login_email@example.com',
    'incrediblygoodpassword',
    to_file = 'pytooter_usercred.secret'
)

# To post, create an actual API instance.

from mastodon import Mastodon

mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
mastodon.toot('Tooting from Python using #mastodonpy !')
