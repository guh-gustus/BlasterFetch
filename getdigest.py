from typing import no_type_check, TypedDict, Final
from bs4.element import AttributeValueList, ResultSet
import requests
import json
import argparse
import datetime
from enum import IntEnum
from bs4 import BeautifulSoup, SoupStrainer, Tag

DATE_FORMAT: Final[str] = "%A, %B %d, %Y"

DAILY_BLAST_URL: Final[str] = "https://webapps.mines.edu/DailyBlast/Home/"

HEADERS: Final[dict[str, str]] = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
}

FILEPATH = "daily_blasts.json"

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--force", action="store_true", help="Force an attempt to pull the digest")
args = parser.parse_args()

class DigestItem(TypedDict):
    title: str
    description: str
    url: str


class DigestCategory(TypedDict):
    digest_items: list[DigestItem]


class DigestDate(TypedDict):
    categories: dict[str, DigestCategory]


class Digests(TypedDict):
    dates: dict[str, DigestDate]


class SyncStatus(IntEnum):
    UP_TO_DATE = 0
    NO_DIGESTS_TODAY = 1
    SUCCESS = 2

class Weekend(IntEnum):
    SATURDAY = 5
    SUNDAY = 6

@no_type_check
def parse_digest_to_dict(digest: Tag) -> DigestItem:
    title_tag: Tag = digest.div.a
    description: str = title_tag.parent.next_sibling.text
    title: str = title_tag.text
    url: str | AttributeValueList = title_tag["href"]

    return {"title": title, "description": description, "url": url}


def is_unscraped_date(tag: Tag, date_strs: list[str]) -> bool:
    try:
        assert tag.name == "td" and (
            tag["class"] == "DigestCategoryDate"
            or tag["class"] == ["DigestCategoryDate"]
        )
        text = tag.text
        date = datetime.date.strptime(text, DATE_FORMAT)
        assert str(date) not in date_strs
        return True
    except ValueError, AssertionError, KeyError:
        return False


def load_saved_digests(filepath: str) -> Digests | SyncStatus:

    today = datetime.date.today()
    if (today.weekday() in Weekend
        and not args.force):
        return SyncStatus.NO_DIGESTS_TODAY

    with open("daily_blasts.json", "r") as saved_digest:
        digests: Digests = json.load(saved_digest)
    
    if args.force:
        return digests

    if str(today) in digests: 
        # print("Already up to date!")
        return SyncStatus.UP_TO_DATE
    else:
        return digests


def get_dates_to_sync(
    url: str, headers: dict[str, str], date_strs: list[str]
) -> SyncStatus | ResultSet[Tag]:

    daily_blast_doc = requests.get(url, headers)
    parse_only_table = SoupStrainer(["td", "tr"])
    soup = BeautifulSoup(
        daily_blast_doc.text, "html.parser", parse_only=parse_only_table
    )
    dates_to_sync: ResultSet[Tag] = soup.find_all(lambda tag: is_unscraped_date(tag, date_strs)
    )

    if not dates_to_sync:
        # print("No daily blast yet")
        return SyncStatus.NO_DIGESTS_TODAY
    else:
        return dates_to_sync


@no_type_check
def parse_document(dates_to_sync: ResultSet[Tag], digests: Digests) -> Digests:
    for date_tag in dates_to_sync:
        date_text: str = date_tag.get_text(strip=True)
        date = str(datetime.date.strptime(date_text, DATE_FORMAT))
        category = ""
        digests[date] = {}

        for row in date_tag.parent.next_siblings:
            match row.td.get("class"):
                case ["DigestCategoryDate"]:
                    break
                case ["DigestCategoryHeader"]:
                    category: str = row.td.text
                    digests[date][category] = []
                case None:
                    digests[date][category].append(parse_digest_to_dict(row.td))

            row = row.find_next_sibling("tr")

    return digests


def sync_daily_blast() -> SyncStatus:
    loaded: Digests | SyncStatus = load_saved_digests(FILEPATH)
    if isinstance(loaded, SyncStatus):
        return loaded
    else:
        digests: Digests = loaded

    dates_to_sync: SyncStatus | ResultSet[Tag] = get_dates_to_sync(
        DAILY_BLAST_URL, HEADERS, list(digests.keys())
    )

    if isinstance(dates_to_sync, SyncStatus):
        return dates_to_sync

    digests: Digests = parse_document(dates_to_sync, digests)

    with open(FILEPATH, "w") as output_file:
        json.dump(digests, output_file, indent=1)

    return SyncStatus.SUCCESS

if __name__ == "__main__":
    print(sync_daily_blast().name)