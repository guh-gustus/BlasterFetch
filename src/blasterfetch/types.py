from typing import TypedDict, TypeAlias
from .enums import Categories


class Digest(TypedDict):
    title: str
    description: str
    url: str

DigestCategories: TypeAlias = dict[Categories, list[Digest]]
DigestDateManager: TypeAlias = dict[str, DigestCategories]

class WrongTypeRecieved(RuntimeError):
    def __init__(self, content_type: str, *args):
        super().__init__(f"Fetching Failed. Expected HTML, recieved {content_type}")

class NoNewBlasts(RuntimeError):
    def __init__(self, *args):
        super().__init__("Saved Blasts Are Up to Date. No longer fetching from remote.")

class WebpageFormatError(RuntimeError):
    def __init__(self, *args):
        super().__init__("Parsing fetched results failed: Webpage formatted improperly.")

class DateNotFoundError(RuntimeError):
    def __init__(self, *args):
        super().__init__("Rendering Failed: Selected Date Not Found")