# PDX-lkmu - Portland Linux Kernel Meetup
This is where we post the public web and calendar for the monthly Portland Linux Kernel Meetup.

Each commit to this repo automatically updates the static web site at https://ikluft.github.io/pdx-lkmu/ .

_Contents_

* [Info for participants](#info-participants)
    * [Setting up a local preview](#setup-preview)
    * [Structure of the pdx-lkmu repo](#repo-structure)
    * [Adding a post, including newly-scheduled meetups](#add-post)
* [Current status](#current-status)

<a name="info-participants"></a>
## Info for participants
For participants authorized to update the repository, here's how to set up your local environment to work on it. It uses the Python-based [Pelican static web site generator](https://docs.getpelican.com/en/latest/). Each commit to the main branch triggers a GitHub Actions workflow to deploy the contents to the live web site.

<a name="setup-preview"></a>
### Setting up a local preview
For work on the site, you can also install Pelican on your local system to preview your work. To set up your local environment on a Linux or other POSIX-compatible system:

* Make sure you have a current version of Python installed. The GitHub Action which deploys the site uses 3.13.
* install Pelican (based on the [quickstart docs](https://docs.getpelican.com/en/latest/quickstart.html))

 python -m pip install "pelican[markdown]" icalendar pytz recurrent

* Use git to grab your copy of the web site repository from https://github.com/ikluft/pdx-lkmu
* the Pelican quickstart process has already been done in that directory
    * [content](content) contains the static web site files
    * [pelicanconf.py](pelicanconf.py) and [publishconf.py](publishconf.py) are the Pelican configuration files
* run Pelican locally (on http://localhost:8000/ unless you change the host or port parameters) to view the static site in your git workspace

    ./run-pdx-lkmu

The original instructions just said to run "pelican --autoreload --listen". But there were differences from the site deployment. So the run-pdx-lkmu script adds customizations which better sync up with the GitHub Actions build process. That's intended to make the local simulated site generator as much as possible like the GitHub site deploy upon each commit.

<a name="repo-structure"></a>
### Structure of the pdx-lkmu repo

Here is the directory structure of the pdx-lkmu repo:

* [top](.) - configuration files
    * [content](content) - each file here is a post in the timeline
        * [category](category) - optional content to add to categories
        * [images](images) - image files for use in pages and posts
        * [pages](pages) - static pages not part of the timeline
    * output - not in the repository: the generated site is here in your workspace after run-pdx-lkmu; do not add or commit it to the repo
    * [plugins](plugins) - pelicanconf.py sets this as the place Pelican looks for plugins
        * [pelican-events-plugin](pelican-events-plugin) - git submodule pointing to Makerspace Esslingen's improved fork of the events plugin
    * [templates](templates) - local page templates (such as calendar event list) are placed here without having to develop a whole new theme

<a name="add-post"></a>
### Adding a post, including newly-scheduled meetups

More details are at the Pelican static site generator's [documentation on writing content](https://docs.getpelican.com/en/latest/content.html).

A short summary of what any of our volunteers need for posting in the PDX Linux Kernel Meetup site is included here. Long story made short:

* Add new posts in the content directory.
* Prefix file names with the date in YYYY-MM-DD format so they will sort neatly for years to come. (Note the 'Date:' metadata in the file contains the date & timestamp for the post. You should keep these consistent.)
* Posts are in Markdown format. So use a .md file suffix. Each file starts with some Pelican metadata headers before the Markdown content.
* Use a local preview to check your work.
* The static site will update automatically within minutes when you commit your changes. Errors can be corrected by editing affected files and committing the changes.

Here's how to format a post for a newly-scheduled Portland Linux Kernel Meetup. Substitute [bracketed items] and date stamps YYYY-MM-DD HH:MM with actual info for the event. Timestamps are in Portland local time, "US/Pacific" - it will automatically use standard or daylight time for the time of year. Pelican doesn't recognize time zone suffixes on timestamps so don't use them in this file.

    Title: [month] 2025 Portland Linux Kernel Meetup
    Date: YYYY-MM-DD HH:MM
    Category: Event Posts
    Author: [your name]
    Summary: Portland Linux Kernel Meetup, [month] [day], [year] [time] at [short location]
    Event-start: YYYY-MM-DD HH:MM
    Event-end: YYYY-MM-DD HH:MM
    Event-location: [full location]

    The Portland Linux Kernel Meetup for [month] [year] will be at

        [weekday], [month] [day], [year]
        6:00 PM to 9:00 PM PDT

        [full location]

    [more intro text]

<a name="current-status"></a>
## Current status

The static site generator runs with the pelican-events-plugin. But now it has become obvious that the plugins do not have a way to fill the iCalendar URL field. There is probably no longer an option but to modify the Python code with a custom plugin, possibly as a pull request to submit to Makerspace Esslingen because their modified plugin got us most of the way to what we need.
