import datetime
from copy import deepcopy
from typing import Final

from bs4 import Tag
from bs4.element import ResultSet

from blasterfetch.config import SOURCE_DATE_FORMAT
from blasterfetch.enums import Categories
from blasterfetch.types import Digest, DigestDateManager, WebpageFormatError

def digest_from_tag(digest_tag: Tag) -> Digest:
    assert digest_tag.div is not None and digest_tag.div.a is not None
    title_tag: Tag = digest_tag.div.a

    assert (title_tag.parent is not None
            and title_tag.parent.next_sibling is not None)
    
    description: str = title_tag.parent.next_sibling.text
    
    assert isinstance(title_tag["href"], str)

    return Digest(title=title_tag.text, description=description, url=title_tag["href"])



def format_dates(dates_to_format: ResultSet[Tag], 
                 saved_digests: DigestDateManager) -> DigestDateManager:
    
    current_digests = deepcopy(saved_digests)
    
    for date_tag in dates_to_format:
        date_text: str = date_tag.get_text(strip=True)
        date = str(datetime.date.strptime(date_text, SOURCE_DATE_FORMAT))
        category = Categories.NONE
        current_digests[date] = {}

        assert isinstance(date_tag.parent, Tag)

        for row in date_tag.parent.next_siblings:
            assert isinstance(row, Tag)
            assert row.td
            match row.td.get("class"):
                case ["DigestCategoryDate"]:
                    break
                case ["DigestCategoryHeader"]:
                    category: Categories = Categories(row.td.text)
                    current_digests[date][category] = []
                case None:
                    current_digests[date][category].append(digest_from_tag(row.td))

            row = row.find_next_sibling("tr")

    return current_digests

def parse(dates: ResultSet[Tag],
          saved_digests: Final[DigestDateManager]) -> DigestDateManager:

    try:
        new_digests = format_dates(dates, saved_digests)
    except AssertionError:
        raise WebpageFormatError()
    
    return new_digests


if __name__ == "__main__":
    print(parse().name)