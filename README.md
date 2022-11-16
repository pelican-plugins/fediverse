# Pelican-toot
A Pelican plugin to publish content on Mastodon

## THIS IS A VERY EARLY STAGE OF DEVELOPMENT 
## DO NOT USE!!

====================================================================================
TEST - TEST - TEST
====================================================================================

Hacked from [Pelican-tweet](https://github.com/mpaglia0/Pelican-tweet).

Needs Python > 3.0

## How it works

*Pelican-toot* will search your contents for articles (actually ALL contents except pages) that are not in a `draft` status.

On its first run it creates a file called `posted_on_Mastodon.txt` in your Pelican root directory.

Then it tries to post all eligible articles to Mastodon and - if post routine returns no errors - writes article URL in `posted_on_Mastodon.txt`.

On every further run it matches the actual articles list with the list in `posted_on_Mastodon.txt` file and posts only new articles (and writes them in `posted_on_Mastodon.txt`).

## Mastodon APIs

In order to publish on Mastodon you need to enter in `publishconf.py` the following information:

TODO
``` python
MASTODON_CONSUMER_KEY = ''
...
```

This plugin depends on [Mastodon.py](https://github.com/halcy/Mastodon.py).
