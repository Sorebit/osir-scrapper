from dataclasses import dataclass
from typing import Awaitable


@dataclass
class GroupData:
    time: int
    group: str
    people: int

RawGroupsData = dict
