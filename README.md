# Fediverse

A Pelican plugin to publish content on the Fediverse

:warning: Under development. Presently only Mastodon is supported. DEVELOPERS NEEDED!

:warning: Needs Python > 3.0

## How it works (Mastodon)

*Fediverse* will search your contents for articles (actually ALL contents except pages) that are not in a `draft` status.

On its first run it creates a file called `posted_on_Mastodon.txt` in your Pelican root directory populated with all your article URLs.

Then it tries to post all eligible articles to Mastodon and - if post routine returns no errors - writes posted article URLs in `posted_on_Mastodon.txt`.

On every further run it matches the actual articles list with the list in `posted_on_Mastodon.txt` file and posts only new articles (and writes them in `posted_on_Mastodon.txt`).

*Fediverse* is at its very first stage of development, but it is already usable in product environments.

This release can publish:

- Title of article
- Body of article
- hashtag(s) if any

Title is taken from `article.title`

Body is taken from `article.summary` with standard Pelican configuartion i.e. length trimmed to 50 words and summary ends with `...` OR with parameters you set in `pelicanconf.py` (`SUMMARY_MAX_LENGTH` and `SUMMARY_END_SUFFIX`).

If the total length of the post exceeds MAX length allowed from Mastodon, then *Fediverse* will trim `article.summary` accordingly.

Hashtag(s) are taken - if any - from `article.tags` and concatenated separating each of them with commas.

Pelican can nicely handle tags with whitespaces (for example `#My nice article`) but in Mastodon they must be written without. For this reason all whitespaces from Pelican hashtags will be removed before publishing (`#Mynicearticle`).

## Mastodon APIs

This plugin depends on [Mastodon.py](https://github.com/halcy/Mastodon.py).

In order to publish on Mastodon you need to enter in `.env` file, on the site root directory, the following information:

``` python
MASTODON_BASE_URL="URL of your Mastodon instance. For example https://mastodon.social"
MASTODON_USERNAME="Your username for Mastodon login"
MASTODON_PASSWORD="You password for Mastodon login"
```

There is no need to register an app in your Mastodon profile because *Fediverse* will do it for you!

On every run *Fediverse* looks for a file called `pelicanfediverse_clientcred.secret` and - if it is not found - it gets in touch with Mastodon, creates an app called *PelicanFediverse* and writes API keys and other necessary information in this file.

If you **cancel** this file *Fediverse* will create another app on its next run (this could be done in case of problem despite the fact Mastodon advise this is NOT a good behaviour since app should be created only once).

## parameters

In `pelicanconf.py` some new parameters can be defined

 - **MASTODON_VISIBILITY** : Set post's visiblity on mastodon. Can be 'direct', 'private', 'unlisted' or 'public'. Default value = 'direct' 
More details : https://mastodonpy.readthedocs.io/en/stable/05_statuses.html#writing 
 - **MASTODON_READ_MORE** : Text to add at the end of the post, before link to the pelican's article. Default value = 'Read more: '

``` Python
MASTODON_VISIBILITY='direct'
MASTODON_READ_MORE='Read more: '
``` 