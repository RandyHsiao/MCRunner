from typing import List
from .bar import Bar

class BarSeries:
    def __init__(self, bars: List[Bar], field: str):
        if bars is None:
            raise ValueError("bars must not be null")
        if not hasattr(Bar, field):
            raise ValueError(f"{field} is not a valid Bar field")
        self._bars = bars
        self._field = field

    def __getitem__(self, bars_ago: int):
        if bars_ago < 0:
            raise IndexError("Can't look into the future!")
        index = len(self._bars) - 1 - bars_ago
        if index < 0:
            raise IndexError(f"{bars_ago} is too far back! There are only {len(self._bars)} bars")
        return getattr(self._bars[index], self._field)

    @property
    def Value(self):
        return self[0]
