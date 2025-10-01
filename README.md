# PDX-lkmu - Portland Linux Kernel Meetup
This is where we post the public web and calendar for the monthly Portland Linux Kernel Meetup.

Each commit to this repo automatically updates the static web site at https://ikluft.github.io/pdx-lkmu/ .

_Contents_

* [Info for participants](#info-participants)
    * [Setting up a local preview](#setup-preview)
    * [Structure of the pdx-lkmu repo](#repo-structure)
    * [Adding a post, including newly-scheduled meetups](#add-post)
        * [Automated method of creating a post for a new meetup](#add-post-automatic)
        * [Manual method of creating a post for a new meetup](#add-post-manual)
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

<a name="add-post-automatic"></a>
#### Automated method of creating a post for a new meetup

You can generate a post text by running with a parameter of the ISO8601 date of the meetupi (i.e. format a date like 2025-09-18):

    ./gen_lkmu_event.py YYYY-MM-DD

That command creates a text file in the contents/ directory named for the event date. For example, './gen_lkmu_event.py 2025-09-18' would try to create 2025-09-18-meetup.md - except that file already exists and would error out. You should run it in your git workspace. Then use 'git add ...', 'git commit ...' and 'git push' to update the git repo. A rebuild of the web site will be triggered when you commit.

<a name="add-post-manual"></a>
#### Manual method of creating a post for a new meetup

Here's how to manually format a post for a newly-scheduled Portland Linux Kernel Meetup. Substitute [bracketed items] and date stamps YYYY-MM-DD HH:MM with actual info for the event. Timestamps are in Portland local time, "US/Pacific" - it will automatically use standard or daylight time for the time of year. Pelican doesn't recognize time zone suffixes on timestamps so don't use them in this file.

    Title: ${month} ${year} Portland Linux Kernel Meetup
    Date: ${post_date}
    Category: Event Posts
    Author: ${author}
    Summary: Portland Linux Kernel Meetup on ${month} ${day}, ${year} ${start_time} at ${location_short}
    Event-start: ${event_start}
    Event-end: ${event_end}
    Event-location: ${location_name}, ${location_street}, ${location_city}
    Event-url: ${url}
    Event-geo: ${location_geo}
    Event-categories: MEETING,PDXLKMU,Linux,Kernel

    The Portland Linux Kernel Meetup for ${month} ${year} will be at...

    * Date: ${weekday}, ${month} ${day}, ${year}
    * Time: ${start_time} to ${end_time} ${time_zone}
    * Location: ${location_name}, ${location_street}, ${location_city}

    Come enjoy a beverage and chat with other people who are interested in the Linux kernel.
    All experience levels are welcome. This is a friendly and casual meetup.

    [more intro text if needed for the specific date]

<a name="current-status"></a>
## Current status

As of September 2025:

After failing to get the legacy (2015) events plugin to generate iCalendar files with support for the URL field, Ian had to update the plugin. The static site generator now uses our [pelican-events plugin](https://github.com/ikluft/pelican-events). This builds on the 2015 events plugin and fixes/extensions by Makerspace Esslingen (Germany). The updated plugin complies with Pelican's current requirement that it is discoverable as a Python module whose name is prefixed with pelican.plugins.* .

Work is in progress adding tests and preparing to submit it to PyPI.
