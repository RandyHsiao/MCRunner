from typing import List, Any

class Bar:
    def __init__(self, time, high, low, open, close, volume):
        self.time = time
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.volume = volume

class BarSeries:
    def __init__(self, bars, field_name):
        self.bars = bars
        self.field_name = field_name

    def __getitem__(self, bars_ago: int) -> Any:
        if bars_ago < 0:
            raise IndexError("Can't look into the future!")

        count = len(self.bars)
        index = count - 1 - bars_ago

        if index < 0:
            raise IndexError(f"{index} is too far back! There are only {count} bars")

        bar = self.bars[index]
        value = getattr(bar, self.field_name)
        return value

    @property
    def value(self):
        return self[0]

class bars:
    def __init__(self):
        self._bars = []

    @property
    def bars(self):
        return self._bars

    @property
    def current_bar(self):
        index = len(self._bars) - 1
        if index < 0:
            raise IndexError()
        return index

    @property
    def high_value(self):
        return self._bars[self.current_bar].high

    @property
    def low_value(self):
        return self._bars[self.current_bar].low

    @property
    def open_value(self):
        return self._bars[self.current_bar].open

    @property
    def close_value(self):
        return self._bars[self.current_bar].close

    @property
    def volume_value(self):
        return self._bars[self.current_bar].volume

    @property
    def time_value(self):
        return self._bars[self.current_bar].time

    @property
    def last_bar_time(self):
        last_bar = self.current_bar - 1
        if last_bar < 0:
            raise IndexError()
        return self._bars[last_bar].time

    @property
    def time(self):
        return BarSeries(self._bars, "time")

    @property
    def high(self):
        return BarSeries(self._bars, "high")

    @property
    def low(self):
        return BarSeries(self._bars, "low")

    @property
    def open(self):
        return BarSeries(self._bars, "open")

    @property
    def close(self):
        return BarSeries(self._bars, "close")

    @property
    def volume(self):
        return BarSeries(self._bars, "volume")

    def add_bar(self, bar: Bar):
        self._bars.append(bar)

class PlayableBars(bars):
    def __init__(self, bars_to_play: List[Bar]):
        super().__init__()
        self.bars_to_play = bars_to_play

    def play(self, action):
        self._bars.clear()
        for bar in self.bars_to_play:
            self._bars.append(bar)
            action(bar)
        self.bars_to_play = None