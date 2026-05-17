from typing import Final, TypeVar, TypedDict
from enum import IntEnum, StrEnum

SOURCE_DATE_FORMAT: Final[str] = "%A, %B %d, %Y"
DAILY_BLAST_URL: Final[str] = "https://webapps.mines.edu/DailyBlast/Home/"
SAVE_FILE_PATH: Final[str] = "daily_blasts.json"

T = TypeVar("T")

class SyncStatus(IntEnum):
    UP_TO_DATE = 0
    NO_DIGESTS_TODAY = 1
    SUCCESS = 2

class Categories(StrEnum):
    CLOSURES = "Closures and Outages"
    EMPLOYEE = "Employee and Benefits News"
    DEADLINES = "Important Deadlines"
    CAMPUS_ANNOUNCEMENTS = "Campus Announcements"
    CAMPUS_EVENTS = "Campus Events"
    CAREER = "Career, Training and Professional Development Opportunities"
    CLUB_MEETINGS = "Club Meetings"
    LECTURES = "Academic Lectures"
    ATHLETICS = "Athletics and Rec Sports"
    NONE = ""
    
class Digest(TypedDict):
    title: str
    description: str
    url: str

DigestCategories = dict[Categories, list[Digest]]


DigestDateManager = dict[str, DigestCategories]

SyncResult = T | SyncStatus

DIGEST_DISPLAY_WIDTH = 40
