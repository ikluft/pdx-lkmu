#!/usr/bin/env python3
"""gen_lkmu_event.py - generate a new event for Portland Linux Kernel Meetup (PDX LKMU) from a template.

written by Ian Kluft
"""

import argparse
import os
import pwd
import sys
from datetime import date, datetime, time
from pathlib import Path
from string import Template
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import validators

#
# functions for initializing constants need to be first
#


def get_user_name() -> str:
    """Get user name as default author name."""
    gecos = pwd.getpwuid(os.getuid())[4]
    if gecos is not None and len(gecos) > 0:
        return gecos
    return pwd.getpwuid(os.getuid())[0]


#
# constants
#

# default values for CLI arguments
PDX_LKMU_DEFAULTS = {
    "author": get_user_name(),
    "start_time": "18:00",
    "end_time": "21:00",
    "time_zone": "US/Pacific",
    "url": "https://ikluft.github.io/pdx-lkmu/",
    "location": "0",
}

# event locations
PDX_LKMU_LOCATIONS = [
    {
        "short": "Lucky Lab on Quimby",
        "name": "Lucky Labrador Beer Hall",
        "street": "1945 NW Quimby St",
        "city": "Portland, Oregon 97209 US",
        "geo": "45.53371;-122.69174",
    },
]

# event article template text
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

#
# exceptions
#


class ScriptError(Exception):
    """Exception intended to be caught and print its message attribute, no stack trace."""

    def __init__(self, message):  # noqa: D107
        self.message = message
        super().__init__(self.message)


class InvalidDateError(ScriptError):
    """Report invalid date."""

    def __init__(self, err: str):  # noqa: D107
        super().__init__(f"event date must be in YYYY-MM-DD format: {err}")


class InvalidTimeError(ScriptError):
    """Report invalid time."""

    def __init__(self, desc: str, err: str):  # noqa: D107
        super().__init__(f"event {desc} time must be in 24-hour HH:MM or HH:MM:SS format: {err}")


class InvalidTzError(ScriptError):
    """Report invalid time zone."""

    def __init__(self, tz_str: str, err: str):  # noqa: D107
        super().__init__(f"unrecognized time zone {tz_str}: {err}")


class InvalidURLError(ScriptError):
    """Report invalid URL."""

    def __init__(self, url: str, err: str):  # noqa: D107
        super().__init__(f"URL failed validation: {url} - reason: {err}")


class InvalidLocationError(ScriptError):
    """Report invalid location."""

    def __init__(self, loc_num: int, max_loc: int):  # noqa: D107
        super().__init__(f"location number must be 0-{max_loc}, got {loc_num}")


class ContentDirNotFoundError(ScriptError):
    """Report the content directory was not found."""

    def __init__(self, content_path: Path):  # noqa: D107
        super().__init__(f"'content' directory ({content_path}) does not exist - run script in PDX-LKMU git workspace")


class ContentNotDirError(ScriptError):
    """Report that the content directory path is occupied by a non-directory."""

    def __init__(self, content_path: Path):  # noqa: D107
        super().__init__(f"'content' directory ({content_path}) path occupied by non-directory - can't create files")


class EventFileExistsError(ScriptError):
    """Report that the event file already exists."""

    def __init__(self, event_path: Path):  # noqa: D107
        super().__init__(f"event file exists and will not be overwritten: {event_path}")

#
# functions
#


def get_parsed_args() -> argparse.Namespace:
    """Parse command line arguments and return Namespace structure with their keys & values."""
    parser = argparse.ArgumentParser()
    parser.add_argument("date")
    parser.add_argument("--quiet", action=argparse.BooleanOptionalAction)
    parser.add_argument("--author")
    parser.add_argument("--start_time", "--start-time")
    parser.add_argument("--end_time", "--end-time")
    parser.add_argument("--time_zone", "--time-zone", "--tz")
    parser.add_argument("--url")
    parser.add_argument("--location", type=int)
    return parser.parse_args()


def dt_to_ical(dt: datetime) -> str:
    """Convert datetime to iCalendar date/time string."""
    return dt.strftime("%Y-%m-%d %H:%M")


def prompt_input(prompt: str, field_name: str, args: argparse.Namespace) -> str:
    """Display a prompt and get user input, including default value if nothing was entered."""
    if field_name in vars(args) and vars(args)[field_name] is not None:
        return vars(args)[field_name]
    default = PDX_LKMU_DEFAULTS[field_name]
    if args.quiet:
        return default
    response = input(f"{prompt} [{default}]: ")
    if len(response) == 0:
        return default
    return response


def parse_date(date_str: str) -> date:
    """Parse and validate a date string, ignore return value if only validating format."""
    try:
        event_date = date.fromisoformat(date_str)
    except ValueError as e:
        raise InvalidDateError(err=e) from e
    return event_date


def parse_time(time_str: str, desc: str) -> time:
    """Parse and validate a time-of-day string, ignore return value if only validating format."""
    try:
        time_obj = time.fromisoformat(time_str)
    except ValueError as e:
        raise InvalidTimeError(desc=desc, err=e) from e
    return time_obj


def parse_tz(tz_str: str) -> ZoneInfo:
    """Parse and validate a time zone string, ignore return value if only validating format."""
    try:
        tz = ZoneInfo(tz_str)
    except (TypeError, ZoneInfoNotFoundError) as e:
        raise InvalidTzError(tz_str=tz_str, err=e) from e
    return tz


def validate_url(url: str) -> None:
    """Validate URL formatting, otherwise raise exception."""
    try:
        result = validators.url(url)
        if isinstance(result, Exception):
            raise result
    except validators.utils.ValidationError as e:
        raise InvalidURLError(url=url, err=e) from e


def validate_location(loc_num: int) -> None:
    """Validate location number, otherwise raise exception."""
    max_loc = len(PDX_LKMU_LOCATIONS) - 1
    if loc_num < 0 or loc_num > max_loc:
        raise InvalidLocationError(loc_num=loc_num, max_loc=max_loc)


def validate_args(args: argparse.Namespace) -> None:
    """Verify values of provided arguments, raise exception for failure."""
    parse_date(args.date)
    if args.start_time is not None:
        parse_time(args.start_time, "start")
    if args.end_time is not None:
        parse_time(args.end_time, "end")
    if args.time_zone is not None:
        parse_tz(args.time_zone)
    if args.location is not None:
        validate_location(args.location)
    if args.url is not None:
        validate_url(args.url)


def get_event_path(params: dict) -> Path:
    """Get event file path and require it doesn't already exist."""
    content_path = Path("content")
    if not content_path.exists():
        raise ContentDirNotFoundError(content_path)
    if not content_path.is_dir():
        raise ContentNotDirError(content_path)
    event_path = content_path / (params["date"] + "-meetup.md")
    if event_path.exists():
        raise EventFileExistsError(event_path=event_path)
    return event_path


def get_meeting_params() -> dict:
    """Get parameters from user input, with defaults from command-line."""
    # initialize empty parameters
    params = {}

    # parse command line
    args = get_parsed_args()
    validate_args(args)

    # parse date and generate related parameters
    event_date = parse_date(args.date)
    params['date'] = event_date.isoformat()
    params['weekday'] = event_date.strftime("%A")
    params['year'] = event_date.strftime("%Y")
    params['month'] = event_date.strftime("%B")
    params['day'] = str(event_date.day)
    get_event_path(params)  # verify event file doesn't already exist before bothering user with questions

    # process time zone
    params['time_zone'] = prompt_input("time zone", 'time_zone', args)
    tz = parse_tz(params['time_zone'])

    # parse start and end times, generate related parameters
    start_time_str = prompt_input("start time", 'start_time', args)
    event_start_time = parse_time(start_time_str, "start")
    params['start_time'] = event_start_time.strftime("%I:%M %p")
    event_start = datetime.combine(event_date, event_start_time, tzinfo=tz)
    params['event_start'] = dt_to_ical(event_start)
    end_time_str = prompt_input("end time", 'end_time', args)
    event_end_time = parse_time(end_time_str, "end")
    params['end_time'] = event_end_time.strftime("%I:%M %p")
    event_end = datetime.combine(event_date, event_end_time, tzinfo=tz)
    params['event_end'] = dt_to_ical(event_end)
    params['post_date'] = dt_to_ical(datetime.now())

    # prompt user for values
    params['author'] = prompt_input("author", 'author', args)
    params['url'] = prompt_input("URL", 'url', args)
    validate_url(params['url'])

    # pull location from table
    if args.location is not None:
        location_num = int(args.location)
    else:
        location_num = int(PDX_LKMU_DEFAULTS["location"])
    validate_location(location_num)
    params['location_short'] = PDX_LKMU_LOCATIONS[location_num]['short']
    params['location_name'] = PDX_LKMU_LOCATIONS[location_num]['name']
    params['location_street'] = PDX_LKMU_LOCATIONS[location_num]['street']
    params['location_city'] = PDX_LKMU_LOCATIONS[location_num]['city']
    params['location_geo'] = PDX_LKMU_LOCATIONS[location_num]['geo']

    # return resulting parameter dict
    return params


def generate_event(params: dict) -> int | str | None:
    """Generate event text from template."""
    template = Template(PDX_LKMU_TEMPLATE)
    event_path = get_event_path(params)
    print(f"generating event file to {event_path}")  # noqa: T201
    with open(event_path, "w", encoding='utf-8') as out_file:
        print(template.safe_substitute(params), file=out_file)

#
# mainline
#


def main() -> int | str | None:
    """Mainline entry point."""
    params = get_meeting_params()
    return generate_event(params)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except ScriptError as e:
        print(f"error: {e.message}", file=sys.stderr)  # noqa: T201
