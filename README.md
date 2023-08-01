# pelican-fediverse

A Pelican plugin to publish content on the Fediverse

!warning! Under development. Presently only Mastodon is supported. DEVELOPERS NEEDED!

Hacked from [Pelican-tweet](https://github.com/mpaglia0/Pelican-tweet).

:warning: Needs Python > 3.0

## How it works (Mastodon)

*pelican-fediverse* will search your contents for articles (actually ALL contents except pages) that are not in a `draft` status.

On its first run it creates a file called `posted_on_Mastodon.txt` in your Pelican root directory populated with all your article URLs.

Then it tries to post all eligible articles to Mastodon and - if post routine returns no errors - writes article URL in `posted_on_Mastodon.txt`.

On every further run it matches the actual articles list with the list in `posted_on_Mastodon.txt` file and posts only new articles (and writes them in `posted_on_Mastodon.txt`).

*pelican-fediverse* is at its very first stage of development, but it is already usable in product environments.

This release can publish:

- Title of article
- Body of article
- hashtag(s) if any

Title is taken from `article.title`

Body is taken from `article.summary` with standard Pelican configuartion i.e. length trimmed to 50 words and summary ends with `...` OR with parameters you set in `pelicanconf.py` (`SUMMARY_MAX_LENGTH` and `SUMMARY_END_SUFFIX`).

If the total length of the post exceeds MAX length allowed from Mastodon, then *pelican-fediverse* will trim `article.summary` accordingly.

Hashtag(s) are taken - if any - from `article.tags` and concatenated separating each of them with commas.

Pelican can handle tags with whitespaces (for example `#My nice article`) without problems but hashtags in Mastodon are all written without. For this reason all whitespaces from Pelican hashtags will be removed before publishing (`#Mynicearticle`).

## Mastodon APIs

This plugin depends on [Mastodon.py](https://github.com/halcy/Mastodon.py).

In order to publish on Mastodon you need to enter in `publishconf.py` the following information:

``` python
MASTODON_BASE_URL = 'URL of your Mastodon instance. For example https://mastodon.social'
MASTODON_USERNAME = 'Your username for Mastodon login'
MASTODON_PASSWORD = 'You password for Mastodon login'
```
There is no need to register an app in your Mastodon profile because *pelican-fediverse* will do it for you!

On every run *pelican-fediverse* looks for a file called `pelicantoot_clientcred.secret` and - if it is not found - it gets in touch with Mastodon, creates an app called *PelicanToot* and writes API keys and other necessary information in this file.

If you **cancel** this file *pelican-fediverse* will create another app on its next run (this could be done in case of problem despite the fact Mastodon advise this is NOT a good behaviour since app should be created only once).
