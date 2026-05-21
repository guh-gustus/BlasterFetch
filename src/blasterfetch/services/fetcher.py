from typing import Final

import requests

from blasterfetch.types import WrongTypeRecieved

DAILY_BLAST_URL: Final[str] = "https://webapps.mines.edu/DailyBlast/Home/"

HEADERS: Final[dict[str, str]] = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
}

def fetch_webpage(headers: dict[str,str] = HEADERS,
                  url: str = DAILY_BLAST_URL) -> str:
    response = requests.get(url, headers)
    content_type = response.headers.get('content-type')

    if 'html' not in content_type:
        raise WrongTypeRecieved(content_type)

    return response.text