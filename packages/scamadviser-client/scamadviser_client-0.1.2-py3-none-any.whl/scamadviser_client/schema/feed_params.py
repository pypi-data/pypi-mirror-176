from enum import Enum

from . import BaseParams


class ListType(str, Enum):
    five_minute = "5-minute"
    hourly = "hourly"
    daily = "daily"


class ListParams(BaseParams):
    type: ListType


class DownloadParams(BaseParams):
    path: str
