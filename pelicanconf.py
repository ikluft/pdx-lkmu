"""configuration for Pelican site generator for Portland Linux Kernel Meetup."""
PLUGIN_EVENTS = {
    'metadata_field_for_summary': 'title',
    'ics_fname': 'calendar.ics',
    'timezone': 'US/Pacific',
}
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'authors', 'archives', 'events_list', 'upcoming_events_list']
THEME_TEMPLATES_OVERRIDES = ["templates"]

AUTHOR = 'Portland Linux Kernel Meetup organizers'
SITENAME = 'Portland Linux Kernel Meetup'
SITEURL = ""

PATH = "content"

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
    ("🗓️ iCalendar for PDX Linux Kernel Meetup", "https://ikluft.github.io/pdx-lkmu/calendar.ics"),
    ("✉️ Google Groups discussion for PDX Linux Kernel Meetup", "https://groups.google.com/g/pdxkernel"),
    # ("Pelican", "https://getpelican.com/"),
)

# Social widget
# from original example, appears to be ignored by Blue Penguin theme
SOCIAL = (
    ("🐧 Drew Fustini @pdp7@fosstodon.org (organizer)", "https://fosstodon.org/@pdp7"),
    ("🐧 John Stultz @jstultz@hachyderm.io (organizer)", "https://hachyderm.io/@jstultz"),
    ("🐧 Ian Kluft @KO6YQ@pnw.zone (web site)", "https://pnw.zone/@KO6YQ"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
