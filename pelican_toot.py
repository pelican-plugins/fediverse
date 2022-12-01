# -*- coding: utf-8 -*-
"""
Post new articles on Mastodon
"""

import sys
import string
from lxml import html
import os.path

import logging
logger = logging.getLogger(__name__)

from pelican import signals

# This plugin needs Mastodon.py (https://github.com/halcy/Mastodon.py)
from mastodon import Mastodon

# Collect the list of articles already published
def read_articleslist():
   try:
      with open('posted_on_Mastodon.txt', 'r') as f:
         result = list(map(str.rstrip, f))
   except IOError:
      result = []
   return result

# Write articles URL list
def write_articleslist(articleslist):
   articleslist.sort()
   with open('posted_on_Mastodon.txt', 'w') as f:
      for article in articleslist:
         f.write("%s\n" % article)

# Collect config info and start the main procedure
def post_on_mastodon(settings, new_posts):
   global mt_base_url
   mt_base_url = settings.get('MASTODON_BASE_URL', '')
   global mt_username
   mt_username = settings.get('MASTODON_USERNAME', '')
   global mt_password
   mt_password = settings.get('MASTODON_PASSWORD', '')

   # check if config file has been duly filled or print an error message and exit
   if mt_base_url == '' or mt_username == '' or mt_password == '':
      logger.warning('Pelican_toot: Mastodon access credentials not configured...')
      sys.exit(9)

   # if pelicantoot_clientcred.secret does not exist it means we have to create the app on Mastodon
   if os.path.exists('pelicantoot_clientcred.secret') == False:
      Mastodon.create_app(
         'PelicanToot',
         api_base_url = mt_base_url,
         to_file = 'pelicantoot_clientcred.secret'
      )

   # Advise the user with an on-screen message
   build_message = 'Publishing on Mastodon: %s\n%s\n'

   for article in new_posts:
      url = article.get_siteurl() + '/' + article.url
      title = article.title
      post = build_message % (title.replace('&nbsp;',' '), url)
      print(post.encode('utf-8'))

   return True

# Extract the list of new posts
def post_updates(generator, writer):
   articleslist = read_articleslist()
   new_posts = []
   for article in generator.articles:
      if article.url not in articleslist:
         new_posts.append(article)

   # we only write the newly found sites to disk if posting them worked. that way we can retry later
   if new_posts:
      if post_on_mastodon(generator.settings, new_posts):
         mastodon = Mastodon(
            client_id = 'pelicantoot_clientcred.secret',
            api_base_url = mt_base_url
         )
         mastodon.log_in(
            mt_username,
            mt_password,
            to_file = 'pelicantoot_usercred.secret'
         )
         mastodon = Mastodon(
            access_token = 'pelicantoot_usercred.secret',
            api_base_url = mt_base_url
         )
         # Actually build the post structure
         for article in new_posts:
            articleslist.append(article.url)
            titlehtmltext = article.title
            titlecleantext = html.fromstring(titlehtmltext)
            title_to_publish = titlecleantext.text_content().strip() + '\n\n'
            articlehtmltext = article.summary
            articlecleantext = html.fromstring(articlehtmltext)
            summary_to_publish = articlecleantext.text_content().strip() + '\n\n'
            if hasattr(article, 'tags'):
               taglist = article.tags
               new_taglist = []
               for i in taglist:
                  new_taglist.append('#' + str(i))
                  tags_to_publish = ', '.join(str(x) for x in new_taglist)
               mastodon_toot = title_to_publish + summary_to_publish + tags_to_publish
            else:
               mastodon_toot = title_to_publish + summary_to_publish
            # check the length of the final post
            toot_maxlength = 480 # Actually 500 but keep a safety gap...
            if len(mastodon_toot) >= toot_maxlength:
               logger.warning('Pelican_toot: your toot exceeds Mastodon max limit... ')
               sys.exit(9)
            else:
               print(mastodon_toot)
               #mastodon.toot(mastodon_toot)
         write_articleslist(articleslist)

def register():
   try:
      signals.article_writer_finalized.connect(post_updates)
   except AttributeError:
      pass
