from datetime import datetime
from typing import TypedDict


class Info(TypedDict):
    name: str
    nickname: str
    birth: datetime
    extra: str
