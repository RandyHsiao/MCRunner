from typing import List
from .bar import Bar
from .bar_series import BarSeries

class Bars:
    def __init__(self):
        self.bars: List[Bar] = []
        self.reload_bar_series()

    def reload_bar_series(self):
        self.Close = BarSeries(self.bars, "Close")
        self.High = BarSeries(self.bars, "High")
        self.Low = BarSeries(self.bars, "Low")
        self.Open = BarSeries(self.bars, "Open")
        self.Time = BarSeries(self.bars, "Time")
        self.Volume = BarSeries(self.bars, "Volume")

    def to_single_data_stream(self):
        return [self]

    @property
    def CurrentBar(self):
        index = len(self.bars) - 1
        if index < 0:
            raise IndexError()
        return index

    @property
    def HighValue(self):
        return self.bars[self.CurrentBar].High

    @property
    def LowValue(self):
        return self.bars[self.CurrentBar].Low

    @property
    def OpenValue(self):
        return self.bars[self.CurrentBar].Open

    @property
    def CloseValue(self):
        return self.bars[self.CurrentBar].Close

    @property
    def VolumeValue(self):
        return self.bars[self.CurrentBar].Volume
