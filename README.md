# Pelican-toot

A Pelican plugin to publish content on Mastodon

Hacked from [Pelican-tweet](https://github.com/mpaglia0/Pelican-tweet).

Needs Python > 3.0

## How it works

*Pelican-toot* will search your contents for articles (actually ALL contents except pages) that are not in a `draft` status.

On its first run it creates a file called `posted_on_Mastodon.txt` in your Pelican root directory populated with all your article tags.

Then it tries to post all eligible articles to Mastodon and - if post routine returns no errors - writes article URL in `posted_on_Mastodon.txt`.

On every further run it matches the actual articles list with the list in `posted_on_Mastodon.txt` file and posts only new articles (and writes them in `posted_on_Mastodon.txt`).

*Pelican-toot* is at its very first stage of development, but it is already usable in product environments.

This release can publish:

- Title of article
- Body of article
- hashtag(s) if any

Title is taken from `article.title`

Body is taken from `article.summary` with standard Pelican configuartion i.e. length trimmed to 50 words and summary ends with `...`

In a future release *Pelican-toot* must have its own configuration parameter for length of text since Mastodon accepts posts with max 500 bytes.

Hashtag(s) are taken - if any - from `article.tags` and concatenated separating each of them with commas.

Pelican can handle tags with whitespaces (for example `#My nice article`) without problems but hashtags in Mastodon are all written without. For this reason all whitespaces from Pelican hashtags will be removed before publishing (`#Mynicearticle`).

Now if your post exceeds this limit you simply will receive the errore message `your toot exceeds Mastodon max limit...`

## Mastodon APIs

This plugin depends on [Mastodon.py](https://github.com/halcy/Mastodon.py).

In order to publish on Mastodon you need to enter in `publishconf.py` the following information:

``` python
MASTODON_BASE_URL = 'URL of your Mastodon instance. For example https://mastodon.social'
MASTODON_USERNAME = 'Your username for Mastodon login'
MASTODON_PASSWORD = 'You password for Mastodon login'
```
There is no need to register an app in your Mastodon profile because *Pelican-toot* will do it for you!

On every run *Pelican-toot* looks for a file called `pelicantoot_clientcred.secret` and - if it is not found - it gets in touch with Mastodon, creates an app called *PelicanToot* and writes API keys and other necessary information in this file.

If you **cancel** this file *Pelican-toot* will create another app on its next run (this could be done in case of problem despite the fact Mastodon advise this is NOT a good behaviour since app should be created only once).
