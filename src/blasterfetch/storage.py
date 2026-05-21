import json
from .types import DigestDateManager

from importlib.resources import files

DATA_FILE = files("blasterfetch").joinpath("data/daily_blasts.json")


class DataManager:
    def load(self) -> DigestDateManager:
        if not DATA_FILE.exists():
            return {}
        return json.loads(DATA_FILE.read_text())

    def save(self, data) -> None:
        DATA_FILE.write_text(json.dumps(data, indent=2))