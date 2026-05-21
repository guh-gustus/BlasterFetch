import datetime

from bs4 import BeautifulSoup, SoupStrainer, Tag
from bs4.element import ResultSet

from blasterfetch.config import SOURCE_DATE_FORMAT
from blasterfetch.types import NoNewBlasts

def confirmation(never_refetch: bool,
                       force_fetch: bool, 
                       date_strs: set[str]):
    if force_fetch: 
        return True
    
    FRIDAY = 4
    today_date = datetime.date.today()
    today = str(today_date)
    
    if today_date.weekday() > FRIDAY and not never_refetch:
        confirm = input("Today is the weekend, which means no new daily blast has been posted. Fetch anyway? [y/N]")
        return confirm[0].lower() == "y"
    
    if today in date_strs and never_refetch: 
        return False
    elif today in date_strs:
        confirm = input("It looks like today's daily blast has already been downloaded. Fetch anyway? [y/N]")
        return confirm[0].lower() == "y"
    else:
        return True

def is_unscraped_date(tag: Tag, date_strs: set[str]) -> bool:
    try:
        assert tag.name == "td" and (
            tag["class"] == "DigestCategoryDate"
            or tag["class"] == ["DigestCategoryDate"]
        )
        text = tag.text
        date = datetime.date.strptime(text, SOURCE_DATE_FORMAT)
        assert str(date) not in date_strs
        return True
    except (ValueError, AssertionError, KeyError):
        return False

def filter(raw_html: str,
           date_strs: set[str]) -> ResultSet[Tag]:

    parse_only_table = SoupStrainer(["td", "tr"])
    soup = BeautifulSoup(
        raw_html, "html.parser", parse_only=parse_only_table
    )

    filtered_tags: ResultSet[Tag] = soup.find_all(
        lambda tag: is_unscraped_date(tag, date_strs)
    )

    if not filtered_tags:
        raise NoNewBlasts()
    
    return filtered_tags