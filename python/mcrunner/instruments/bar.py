from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

class BarType(Enum):
    Live = auto()
    Historic = auto()

@dataclass
class Bar:
    Time: datetime = None
    High: float = 0.0
    Low: float = 0.0
    Open: float = 0.0
    Close: float = 0.0
    Volume: float = 0.0
    BarType: BarType = BarType.Historic
