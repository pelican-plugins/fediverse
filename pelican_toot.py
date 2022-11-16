# -*- coding: utf-8 -*-
"""
Post new articles on Mastodon
"""

import string

import logging
logger = logging.getLogger(__name__)

from pelican import signals

# https://github.com/halcy/Mastodon.py
from mastodon import Mastodon
