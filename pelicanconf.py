"""
configuration settings for Pelican
"""
AUTHOR = 'Portland Linux Kernel Meetup organizers'
SITENAME = 'Portland Linux Kernel Meetup'
SITEURL = ""

PATH = "content"

TIMEZONE = 'US/Pacific'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("PDX Linux Kernel Meetup on Meetup.com", "https://www.meetup.com/portland-linux-kernel-meetup/"),
    # ("Pelican", "https://getpelican.com/"),
)

# Social widget
SOCIAL = (
    ("Drew Fustini", "@pdp7@fosstodon.org"),
    ("John Stultz", "@jstultz@fosstodon.org"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
