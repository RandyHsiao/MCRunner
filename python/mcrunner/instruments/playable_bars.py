from typing import Iterable, Callable
from .bars import Bars
from .bar import Bar

class PlayableBars(Bars):
    def __init__(self, bars_to_play: Iterable[Bar]):
        super().__init__()
        self.bars_to_play = list(bars_to_play)

    def play(self, action: Callable[[Bar], None]):
        for bar in self.bars_to_play:
            self.bars.append(bar)
            self.reload_bar_series()
            action(bar)
        self.bars_to_play = []
