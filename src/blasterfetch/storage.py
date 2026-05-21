import json
from .types import DigestDateManager

from importlib.resources import files
from os import PathLike
from pathlib import Path

DEFAULT_DATA_FILE = files("blasterfetch").joinpath("data/daily_blasts.json")
class DataManager:
    def __init__(self, 
                 data_file: PathLike = DEFAULT_DATA_FILE):
        self.DATA_FILE = Path(data_file)
    
    def load(self) -> DigestDateManager:
        if not self.DATA_FILE.exists():
            return {}
        return json.loads(self.DATA_FILE.read_text())

    def save(self, data) -> None:
        self.DATA_FILE.write_text(json.dumps(data, indent=2))