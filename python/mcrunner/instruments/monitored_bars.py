from typing import Callable, List
from .loadable_bars import LoadableBars
from .bar import Bar

class MonitoredBars(LoadableBars):
    def __init__(self):
        super().__init__()
        self._callbacks: List[Callable[[Bar], None]] = []

    def add_callback(self, cb: Callable[[Bar], None]):
        self._callbacks.append(cb)

    def add_bar(self, bar: Bar):
        super().add_bar(bar)
        for cb in list(self._callbacks):
            cb(bar)

    def to_single_data_stream(self):
        return [self]
