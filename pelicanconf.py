"""
configuration settings for Pelican
"""

PLUGIN_PATHS = ["plugins"]
PLUGINS = ['pelican-events-plugin']
PLUGIN_EVENTS = {
    'metadata_field_for_summary': 'title',
    'ics_fname': 'calendar.ics',
}
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'authors', 'archives', 'events_list']
THEME_TEMPLATES_OVERRIDES = ["templates"]

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

# additional menu items
# used by Blue Penguin theme
MENUITEMS = (
    ('GitHub repo', 'https://github.com/ikluft/pdx-lkmu'),
    ('Linux Kernel', 'https://www.kernel.org/'),
)

# Blogroll
# from original example, appears to be ignored by Blue Penguin theme
LINKS = (
    ("PDX Linux Kernel Meetup on Meetup.com", "https://www.meetup.com/portland-linux-kernel-meetup/"),
    # ("Pelican", "https://getpelican.com/"),
)

# Social widget
# from original example, appears to be ignored by Blue Penguin theme
SOCIAL = (
    ("Drew Fustini @pdp7@fosstodon.org", "https://fosstodon.org/@pdp7"),
    ("John Stultz @jstultz@fosstodon.org", "https://fosstodon.org/@jstultz"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
