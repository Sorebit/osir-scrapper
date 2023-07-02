from dataclasses import dataclass
from datetime import datetime

@dataclass
class GroupData:
    dt: datetime
    group: str
    people: int
