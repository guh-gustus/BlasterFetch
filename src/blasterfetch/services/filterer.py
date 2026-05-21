import datetime

from bs4 import BeautifulSoup, SoupStrainer, Tag
from bs4.element import ResultSet

from blasterfetch.config import SOURCE_DATE_FORMAT
from blasterfetch.types import NoNewBlasts

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