from .bars import Bars
from .bar import Bar

class LoadableBars(Bars):
    def add_bar(self, bar: Bar):
        self.bars.append(bar)
        self.reload_bar_series()
