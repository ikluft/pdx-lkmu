#!/usr/bin/env python3
"""
gen_lkmu_event.py - generate a new event for Portland Linux Kernel Meetup (PDX LKMU) from a template
written by Ian Kluft
"""

import argparse
from datetime import date, time, datetime
from zoneinfo import ZoneInfo
import sys
import os
from pathlib import Path
import pwd
from string import Template

PDX_LKMU_DEFAULTS = {
    "start_time": "18:00:00",
    "end_time": "21:00:00",
    "time_zone": "US/Pacific",
    "url": "https://ikluft.github.io/pdx-lkmu/",
    "location": "0",
}
PDX_LKMU_LOCATIONS = [
    {
        "short": "Lucky Lab on Quimby",
        "name": "Lucky Labrador Beer Hall",
        "street": "1945 NW Quimby St",
        "city": "Portland, Oregon 97209 US",
        "geo": "45.53371;-122.69174",
    },
]
PDX_LKMU_TEMPLATE = \
    '''Title: ${month} ${year} Portland Linux Kernel Meetup
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
All experience levels are welcome. This is a friendly and casual meetup.'''


class ScriptError(Exception):
    """Exception intended to be caught and print message attribute, no stack trace."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_user_name() -> str:
    """get user name as default author name."""
    gecos = pwd.getpwuid(os.getuid())[4]
    if gecos is not None and len(gecos) > 0:
        return gecos
    username = pwd.getpwuid(os.getuid())[0]
    return username


def dt_to_ical(dt: datetime) -> str:
    """convert datetime to iCalendar date/time string."""
    return dt.strftime("%Y:%m:%d %H:%M")


def prompt_input(prompt: str, default: str) -> str:
    """Display a prompt and get user input, including default value if nothing was entered."""
    response = input(f"{prompt} [{default}]: ")
    if len(response) == 0:
        return default
    return response


def get_event_path(params: dict) -> Path:
    """get event file path and require it doesn't already exist"""
    content_path = Path(Path.cwd(), "content")
    if not content_path.exists():
        raise ScriptError("'content' directory does not exist - this should be run in a PDX-LKMU git workspace")
    if not content_path.is_dir():
        raise ScriptError("'content' must be a directory in order to create files in it")
    event_path = content_path / (params["date"] + "-meetup.md")
    if event_path.exists():
        raise ScriptError(f"{event_path} exists - script will not overwrite it")
    return event_path


def get_meeting_params() -> dict:
    """get parameters from user input, with defaults from command-line"""
    # initialize empty parameters
    params = {}

    # parse command line
    parser = argparse.ArgumentParser()
    parser.add_argument("date")
    parser.add_argument("--author", default=get_user_name())
    parser.add_argument("--start_time", default=PDX_LKMU_DEFAULTS["start_time"])
    parser.add_argument("--end_time", default=PDX_LKMU_DEFAULTS["end_time"])
    parser.add_argument("--time_zone", default=PDX_LKMU_DEFAULTS["time_zone"])
    parser.add_argument("--url", default=PDX_LKMU_DEFAULTS["url"])
    parser.add_argument("--location", default=PDX_LKMU_DEFAULTS["location"])
    args = parser.parse_args()

    # parse date and generate related parameters
    event_date = date.fromisoformat(args.date)
    params['date'] = event_date.isoformat()
    params['weekday'] = event_date.strftime("%A")
    params['year'] = event_date.strftime("%Y")
    params['month'] = event_date.strftime("%B")
    params['day'] = str(event_date.day)
    get_event_path(params)  # verify event file doesn't already exist before bothering user with questions

    # process time zone
    params['time_zone'] = prompt_input("time zone", args.time_zone)
    tz = ZoneInfo(params['time_zone'])

    # parse start and end times, generate related parameters
    start_time_str = prompt_input("start time", args.start_time)
    event_start_time = time.fromisoformat(start_time_str)
    params['start_time'] = event_start_time.strftime("%I:%M %p")
    event_start = datetime.combine(event_date, event_start_time, tzinfo=tz)
    params['event_start'] = dt_to_ical(event_start)
    end_time_str = prompt_input("end time", args.end_time)
    event_end_time = time.fromisoformat(end_time_str)
    params['end_time'] = event_end_time.strftime("%I:%M %p")
    event_end = datetime.combine(event_date, event_end_time, tzinfo=tz)
    params['event_end'] = dt_to_ical(event_end)
    params['post_date'] = dt_to_ical(datetime.now())

    # prompt user for values
    params['author'] = prompt_input("author", args.author)
    params['url'] = prompt_input("URL", args.url)

    # pull location from table
    location_num = int(args.location)
    params['location_short'] = PDX_LKMU_LOCATIONS[location_num]['short']
    params['location_name'] = PDX_LKMU_LOCATIONS[location_num]['name']
    params['location_street'] = PDX_LKMU_LOCATIONS[location_num]['street']
    params['location_city'] = PDX_LKMU_LOCATIONS[location_num]['city']
    params['location_geo'] = PDX_LKMU_LOCATIONS[location_num]['geo']

    # return resulting parameter dict
    return params


def generate_event(params: dict) -> int | str | None:
    """generate event text from template"""
    template = Template(PDX_LKMU_TEMPLATE)
    event_path = get_event_path(params)
    print(f"generating event file to {event_path}")
    with open(event_path, "w", encoding='utf-8') as out_file:
        print(template.safe_substitute(params), file=out_file)


def main() -> int | str | None:
    """mainline entry point"""
    params = get_meeting_params()
    return generate_event(params)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except ScriptError as e:
        print(f"error: {e.message}", file=sys.stderr)
