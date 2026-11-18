import os
from os import PathLike

import click

from .services import fetcher, filterer, parser, renderer
from .storage import DataManager
from .types import NoNewBlasts


@click.command()
@click.option(
    "--force-fetch",
    "-f",
    default=False,
    is_flag=True,
    help="Attempts to fetch, even if already up to date.",
)
@click.option(
    "--silent",
    "-s",
    default=False,
    is_flag=True,
    help="Just fetches and saves daily blast, prints nothing.",
)
@click.option(
    "--local",
    "-l",
    default=False,
    is_flag=True,
    help="Doesn't try to fetch from remote.",
)
@click.option(
    "--column-width", "-w", default=40, help="Width of printed columns in characters."
)
@click.option(
    "--excluded-categories",
    "-x",
    default="",
    help="comma seperated list of excluded categories. Options are: CLOSURES, EMPLOYEE, DEADLINES, CAMPUS_ANNOUNCEMENTS, CAMPUS_EVENTS, CAREER, CLUB_MEETINGS, LECTURES, ATHLETICS, RESEARCH, EVERY_OREDIGGER",
)
@click.option(
    "--path",
    "-p",
    default="",
    help="File path to save/load Daily Blasts from. Defaults to $XDG_DATA_HOME/blasterfetch/dailyblasts.json",
)
@click.option(
    "--date",
    "-d",
    default="",
    help="Date to print, defaults to most recent. Expected in YYYY-MM-DD format.",
)
@click.option(
    "--fuzzy-date",
    "-z",
    default=False,
    is_flag=True,
    help="Print latest date if selected date isn't found.",
)
@click.option(
    "--never-refetch",
    "-r",
    default=False,
    is_flag=True,
    help="Don't fetch if today's date is already in database, or if it's the weekend"
)
def blasterfetch(
    force_fetch: bool,
    silent: bool,
    local: bool,
    column_width: int,
    excluded_categories: str,
    path: PathLike,
    date: str,
    fuzzy_date: bool,
    never_refetch: bool
) -> None:
    if path == "":
        path = os.path.join(
            os.environ["XDG_DATA_HOME"], "blasterfetch/dailyblasts.json"
        )
    if date == "":
        fuzzy_date = True

    data_manager = DataManager(path)
    saved_blasts = data_manager.load()
    date_strs = set(saved_blasts.keys())
    filtered_dates = None

    if (not local and filterer.confirmation(never_refetch, 
                                            force_fetch, 
                                            date_strs)):
        try:
            raw_html = fetcher.fetch_webpage()
            filtered_dates = filterer.filter(raw_html, date_strs)
        except NoNewBlasts as e:
            if not never_refetch:
                print(e)
    
    if filtered_dates is not None:
        new_blasts = parser.parse(filtered_dates, saved_blasts)
        data_manager.save(new_blasts)
        saved_blasts = new_blasts

    if not silent:
        renderer.render(saved_blasts, date, fuzzy_date, column_width, excluded_categories.split(","))
