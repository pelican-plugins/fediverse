# -*- coding: utf-8 -*-
"""
Post new articles on Mastodon
"""

import sys
import string
from lxml import html
import os.path
from dotenv import load_dotenv

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

   load_dotenv()
   global mt_base_url
   mt_base_url = os.getenv('MASTODON_BASE_URL')
   global mt_username
   mt_username = os.getenv('MASTODON_USERNAME')
   global mt_password
   mt_password = os.getenv('MASTODON_PASSWORD')

   global mt_read_more
   mt_read_more = settings.get('MASTODON_READ_MORE', '')
   global mt_visibility
   mt_visibility = settings.get('MASTODON_VISIBILITY', '')

   # check if config file has been duly filled or print an error message and exit
   if mt_base_url == '' or mt_username == '' or mt_password == '':
      logger.warning('Pelican_fediverse: Mastodon access credentials not configured...')
      sys.exit(9)

   # if pelicantoot_clientcred.secret does not exist it means we have to create the app on Mastodon
   if os.path.exists('pelicanfediverse_clientcred.secret') == False:
      Mastodon.create_app(
         'PelicanFediverse',
         api_base_url = mt_base_url,
         to_file = 'pelicanfediverse_clientcred.secret'
      )

   # Advise the user with an on-screen message. We are ready to publish!
   build_message = 'Publishing on Mastodon: %s (%s)'

   for article in new_posts:
      url = article.get_siteurl() + article.url
      title = article.title
      htmltext = build_message % (title.replace('&nbsp;',' '), url)
      cleantext = html.fromstring(htmltext)
      finaltext = cleantext.text_content().strip()
      print(finaltext)

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
            client_id = 'pelicanfediverse_clientcred.secret',
            api_base_url = mt_base_url
         )
         mastodon.log_in(
            mt_username,
            mt_password,
            to_file = 'pelicanfediverse_usercred.secret'
         )
         mastodon = Mastodon(
            access_token = 'pelicanfediverse_usercred.secret',
            api_base_url = mt_base_url
         )
         # Actually build the post structure
         # First set a maximum length for the final post
         toot_maxlength = 490 # Actually 500 but let's keep a safety gap for miscalculation...
         for article in new_posts:
            articleslist.append(article.url)
            titlehtmltext = article.title
            titlecleantext = html.fromstring(titlehtmltext)
            title_to_publish = titlecleantext.text_content().strip() + '\n\n'
            articlehtmltext = article.summary
            articlecleantext = html.fromstring(articlehtmltext)
            summary_to_publish = articlecleantext.text_content().strip() + '\n'
            read_more = mt_read_more + article.get_siteurl() + '/' + article.url + '\n\n'
            if hasattr(article, 'tags'):
               taglist = article.tags
               new_taglist = []
               for i in taglist:
                  new_taglist.append('#' + str(i))
                  tags_to_publish = ', '.join(str(x).replace(" ", "") for x in new_taglist)
               toot_length = len(title_to_publish) + len(summary_to_publish) + len(read_more) + len(tags_to_publish)
               if toot_length > toot_maxlength:
                  truncate = toot_maxlength - len(title_to_publish) - len(tags_to_publish) - len(read_more) - 4
                  summary_to_publish = summary_to_publish[:truncate] + ' ...' + '\n'
                  mastodon_toot = title_to_publish + summary_to_publish + read_more + tags_to_publish
               else:
                  mastodon_toot = title_to_publish + summary_to_publish + read_more + tags_to_publish
            else:
               toot_length = len(title_to_publish) + len(summary_to_publish) + len(read_more)
               if toot_length > toot_maxlength:
                  truncate = toot_maxlength - len(title_to_publish) - len(read_more) - 4
                  summary_to_publish = summary_to_publish[:truncate] + ' ...' + '\n'
                  mastodon_toot = title_to_publish + summary_to_publish + read_more
               else:
                  mastodon_toot = title_to_publish + summary_to_publish + read_more

            mastodon.status_post(mastodon_toot, visibility=mt_visibility)

         write_articleslist(articleslist)


def register():
   try:
      signals.article_writer_finalized.connect(post_updates)
   except AttributeError:
      pass
