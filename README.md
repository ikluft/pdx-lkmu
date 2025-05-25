# PDX-lkmu - Portland Linux Kernel Meetup
This is where we post the public web and calendar for the monthly Portland Linux Kernel Meetup.

Each commit to this repo automatically updates the static web site at https://ikluft.github.io/pdx-lkmu/ .

## Info for participants
For participants authorized to update the repository, here's how to set up your local environment to work on it. It uses the Python-based [Pelican static web site generator](https://docs.getpelican.com/en/latest/). Each commit to the main branch triggers a Github Actions workflow to deploy the contents to the live web site.

For work on the site, you can also install Pelican on your local system to preview it. To set up your local environment on a Linux or other POSIX-compatible system:

* Make sure you have a current version of Python installed.
* install Pelican (based on the [quickstart docs](https://docs.getpelican.com/en/latest/quickstart.html))

 python -m pip install "pelican[markdown]"

* Grab your copy of the web site repository from https://github.com/ikluft/pdx-lkmu
* the Pelican quickstart process has already been done in that directory
  * [content](content) contains the static web site files
  * [pelicanconf.py](pelicanconf.py) and [publishconf.py](publishconf.py) are the Pelican configuration files
* In another directory (not in the web site content workspace), grab a copy of the Pelican themes with

   git clone --recursive https://github.com/getpelican/pelican-themes

* install the blue-penguin and blue-penguin-dark themes locally

   pelican-themes --install pelican-themes/blue-penguin pelican-themes/blue-penguin-dark

*[... work in progress - to be continued ...]*
