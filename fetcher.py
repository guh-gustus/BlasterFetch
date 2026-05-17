from typing import Final
from bs4.element import ResultSet
import requests
import json
import datetime
from bs4 import BeautifulSoup, SoupStrainer, Tag

from globals import (
    SOURCE_DATE_FORMAT,
    DAILY_BLAST_URL,
    SAVE_FILE_PATH,
    SyncStatus,
    Categories,
    Digest,
    DigestDateManager,
    SyncResult,
)

HEADERS: Final[dict[str, str]] = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
}

def digest_from_tag(digest_tag: Tag) -> Digest:
    assert digest_tag.div is not None and digest_tag.div.a is not None
    title_tag: Tag = digest_tag.div.a

    assert (title_tag.parent is not None
            and title_tag.parent.next_sibling is not None)
    
    description: str = title_tag.parent.next_sibling.text
    
    assert isinstance(title_tag["href"], str)

    return Digest(title=title_tag.text, description=description, url=title_tag["href"])

def load_saved_digests(filepath=SAVE_FILE_PATH) -> DigestDateManager:
    with open(filepath, "r") as saved_digest:
        digests: DigestDateManager = json.load(saved_digest)

    return digests

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

def parse_document(dates_to_sync: ResultSet[Tag], digests: DigestDateManager) -> DigestDateManager:
    for date_tag in dates_to_sync:
        date_text: str = date_tag.get_text(strip=True)
        date = str(datetime.date.strptime(date_text, SOURCE_DATE_FORMAT))
        category = Categories.NONE
        digests[date] = {}

        assert isinstance(date_tag.parent, Tag)

        for row in date_tag.parent.next_siblings:
            assert isinstance(row, Tag)
            assert row.td
            match row.td.get("class"):
                case ["DigestCategoryDate"]:
                    break
                case ["DigestCategoryHeader"]:
                    category: Categories = Categories(row.td.text)
                    digests[date][category] = []
                case None:
                    digests[date][category].append(digest_from_tag(row.td))

            row = row.find_next_sibling("tr")

    return digests

def get_dates_to_sync(
    url: str, 
    headers: dict[str, str], 
    date_strs: set[str]) -> SyncResult[ResultSet[Tag]]:

    today = datetime.date.today().strftime(SOURCE_DATE_FORMAT)
    if today in date_strs:
        return SyncStatus.UP_TO_DATE

    daily_blast_doc = requests.get(url, headers)
    parse_only_table = SoupStrainer(["td", "tr"])
    soup = BeautifulSoup(
        daily_blast_doc.text, "html.parser", parse_only=parse_only_table
    )

    dates_to_sync: ResultSet[Tag] = soup.find_all(
        lambda tag: is_unscraped_date(tag, date_strs)
    )

    if not dates_to_sync:
        return SyncStatus.NO_DIGESTS_TODAY
    else:
        return dates_to_sync

def main() -> SyncResult:
    digests: DigestDateManager = load_saved_digests()
        
    dates_to_sync: SyncResult[ResultSet[Tag]] = get_dates_to_sync(
        DAILY_BLAST_URL, HEADERS, set(digests.keys())
    )

    if isinstance(dates_to_sync, SyncStatus):
        return dates_to_sync

    digests = parse_document(dates_to_sync, digests)

    with open(SAVE_FILE_PATH, "w") as output_file:
        json.dump(digests, output_file, indent=1)

    return SyncStatus.SUCCESS

if __name__ == "__main__":
    print(main().name)