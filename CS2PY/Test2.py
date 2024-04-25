# Importing necessary libraries
import numpy as np
from datetime import datetime, timedelta
from typing import List, TypeVar, Generic

# Defining necessary classes
T = TypeVar('T')

class Bar:
    def __init__(self, time, high, low, open, close, volume):
        self.Time = time
        self.High = high
        self.Low = low
        self.Open = open
        self.Close = close
        self.Volume = volume

class Bars:
    def __init__(self):
        self._bars = []
        self._current_bar = -1

    @property
    def Bars(self):
        return self._bars

    @property
    def CurrentBar(self):
        return self._current_bar

    def UpdateCurrentBar(self):
        self._current_bar = len(self._bars) - 1

    def __getitem__(self, bars_ago):
        if bars_ago < 0:
            raise IndexError("Can't look into the future!")

        index = self.CurrentBar - bars_ago
        if index < 0:
            raise IndexError(f"{bars_ago} is too far back! There are only {self.CurrentBar + 1} bars")

        return self._bars[index]

    @property
    def CloseValue(self):
        return [bar.Close for bar in self._bars]
    
    @property
    def Close(self):
        return BarSeries(self, "Close")
    
    @property
    def Time(self):
        return BarSeries(self, "Time")

    def AddBar(self, bar: Bar):
        self._bars.append(bar)
        self.UpdateCurrentBar()

class VariableSeries:
    def __init__(self):
        self.values = []

    def append(self, value):
        self.values.append(value)

    @property
    def Value(self):
        return self.values[-1] if self.values else None

    def __getitem__(self, bars_ago):
        if bars_ago < 0:
            raise IndexError("Can't look into the future!")

        count = len(self.values)
        index = count - bars_ago - 1

        if index < 0:
            raise IndexError(f"{bars_ago} is too far back! There are only {count} values")

        return self.values[index]

    def __len__(self):
        return len(self.values)

    @property
    def Value(self):
        return self.values[-1] if self.values else None

class BarSeries:
    def __init__(self, bars, field_name):
        self.bars = bars
        self.field_name = field_name

    def _get_field(self, bar):
        if hasattr(bar, self.field_name):
            return getattr(bar, self.field_name)
        else:
            raise AttributeError(f"{self.field_name} is not a valid field of Bar")

    def __getitem__(self, bars_ago):
        if bars_ago < 0:
            raise IndexError("Can't look into the future!")
        
        current_bar = self.bars.CurrentBar
        if bars_ago > current_bar:
            raise IndexError(f"{bars_ago} is too far back! There are only {current_bar + 1} bars available.")

        index = current_bar - bars_ago
        bar = self.bars.Bars[index]
        return self._get_field(bar)

    def __len__(self):
        return len(self.bars.Bars)
      
    @property
    def value(self):
        return self[0]

    def Lowest(self, lookback_period, bars_ago=0):
        values = [self[i] for i in range(bars_ago, bars_ago + lookback_period)]
        return min(values) if values else None

    def Highest(self, lookback_period, bars_ago=0):
        values = [self[i] for i in range(bars_ago, bars_ago + lookback_period)]
        return max(values) if values else None

# Adjusting Play method in PlayableBars to correctly call CalcBar
class PlayableBars(Bars):
    def __init__(self, barsToPlay: List[Bar]):
        self.BarsToPlay = barsToPlay
        self._bars = barsToPlay.copy()
        self._current_bar = len(self._bars) - 1

    def Play(self, action):
        temp_bars = self._bars.copy()
        self._bars.clear()
        self._current_bar = -1

        print(f"Playing bars: {self.BarsToPlay}")  # Debug print
             
        for bar in temp_bars:
            self.AddBar(bar)
            action()

        self.BarsToPlay = None

# class XAverage:
#     def __init__(self, price_series, length):
#         self.values = []
#         self.Length = length
#         self.Price = price_series
#         self.StartCalc()
    
#     def Create(self):
#         pass

#     def StartCalc(self):
#         print(f"self.Price in StartCalc: {self.Price}")  # 添加这行打印语句
#         price_data = [self.Price[i] for i in range(len(self.Price))]

#         print(f"Starting EMA calculation with data: {price_data}")  # Debug print

#         if len(price_data) < self.Length:
#             print("Not enough data to start EMA calculation")  # Debug print
#             return

#         alpha = 2.0 / (self.Length + 1)

#         self.values.append(price_data[0])
#         for i in range(1, len(price_data)):
#             self.values.append(self.values[-1] + alpha * (price_data[i] - self.values[-1]))
#             print(f"Calculating EMA for price: {price_data[i]} at date: {self.Price.bars[i].Time}")  # 添加这行打印语句
          
#     def CaclBar(self):
#         pass

#     def __getitem__(self, bars_ago: int) -> float:
#         if bars_ago < 0 or bars_ago >= len(self.values):
#             raise IndexError("Index out of range")
#         return self.values[bars_ago]

#     @property
#     def Value(self) -> float:
#         return self.values[-1] if self.values else None

class XAverage:
    def __init__(self, price_series, length):
        self.values = []
        self.Length = length
        self.Price = price_series
        print(f"Initializing XAverage with length: {length} and price series: {price_series}")
        self.StartCalc()

    def Create(self):
        pass
    
    def StartCalc(self):
        print(f"Starting XAverage calculation with price series: {self.Price}")
        
        if len(self.Price) < self.Length:
            print(f"Not enough data points to calculate XAverage. Required: {self.Length}, Available: {len(self.Price)}")
            return
        
        alpha = 2.0 / (self.Length + 1)
        
        self.values.append(self.Price[0])
        for i in range(1, len(self.Price)):
            new_value = self.values[-1] + alpha * (self.Price[i] - self.values[-1])
            self.values.append(new_value)
            print(f"Calculated new XAverage value: {new_value} for price: {self.Price[i]}")
        
        print(f"Finished XAverage calculation. Result: {self.values}")
          
    def CalcBar(self):
        pass
    
    def __getitem__(self, bars_ago: int) -> float:
        if bars_ago < 0 or bars_ago >= len(self.values):
            raise IndexError("Index out of range")
        return self.values[bars_ago]
    
    @property
    def Value(self) -> float:
        value = self.values[-1] if self.values else None
        print(f"Returning current XAverage value: {value}")
        return value

    
# Defining the abstract class for studies
class CStudyAbstract:
    def __init__(self, bars):
        self.bars = bars

    def Create(self):
        pass

    def StartCalc(self):
        pass

    def CalcBar(self):
        pass

# Implementing the PriceBreakouts study
class PriceBreakouts(CStudyAbstract):
    def __init__(self, bars):
        super().__init__(bars)
        self.EMALength = 5
        self.LookbackPeriod = 3
        self.EMA = None
        self.lowestClose = None
        self.highestClose = None
        self.emaValues = None

    def Create(self):
        if not self.bars or not hasattr(self.bars, 'Close'):
            raise ValueError("Bars object is required with a Close series available for EMA calculation.")

        self.lowestClose = VariableSeries()
        self.highestClose = VariableSeries()
        self.emaValues = VariableSeries()
        # print(f"self.bars.Close in Create: {self.bars.Close}")  # 添加这行打印语句
        self.EMA = XAverage(self.bars.CloseValue, self.EMALength)
        #self.EMA.StartCalc()

    def CalcBar(self):
        current_bar = self.bars.CurrentBar

        if current_bar < self.LookbackPeriod:
            return

        self.lowestClose.append(self.bars.Close.Lowest(self.LookbackPeriod, 1))
        self.highestClose.append(self.bars.Close.Highest(self.LookbackPeriod, 1))
        self.emaValues.append(self.EMA[current_bar])

        # current_bar = self.bars.CurrentBar
        print(f"Bar {current_bar + 1}:")
        print(f"Current Bar Close: {self.bars.Close[0]}, Previous Bar Close: {self.bars.Close[1]}")
        print(f"Lowest Close in Last {self.LookbackPeriod} Bars: {self.lowestClose.Value}")
        print(f"Highest Close in Last {self.LookbackPeriod} Bars: {self.highestClose.Value}")

        if len(self.emaValues.values) > 0:
            print(f"Latest EMA Value: {self.emaValues[0]}")
            if len(self.emaValues.values) > 1:
                print(f"Previous EMA Value: {self.emaValues[1]}")
        else:
            print("EMA value not available for the current bar")

# Creating simulated data
dates = [datetime.now() - timedelta(days=9-i) for i in range(10)]
prices_open = np.array([100, 101, 102, 103, 104, 105, 106, 107, 108, 109])
prices_high = np.array([105, 106, 107, 108, 109, 110, 111, 112, 113, 114])
prices_low = np.array([95, 96, 97, 98, 99, 100, 101, 102, 103, 104])
prices_close = np.array([102, 103, 104, 105, 106, 107, 108, 109, 110, 111])
volumes = np.array([1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009])

# Creating Bar objects and adding them to a Bars object
bars = Bars()
for i in range(len(dates)):
    bar = Bar(dates[i], prices_high[i], prices_low[i], prices_open[i], prices_close[i], volumes[i])
    bars.AddBar(bar)
    # print(f"Added new bar: Date={bar.Time}, Open={bar.Open}, High={bar.High}, Low={bar.Low}, Close={bar.Close}, Volume={bar.Volume}")

print(f"Close: {[bar.Close for bar in bars._bars]}")
print(f"CloseValues: {bars.CloseValue}")


# Creating a PlayableBars object
playable_bars = PlayableBars(bars.Bars)

# Creating the strategy object and initializing it
strategy = PriceBreakouts(playable_bars)
print(f"Type of bars.Close before creating test_ema: {type(bars.Close)}")
test_ema = XAverage(bars.CloseValue, 5)
print(f"bars.Close before creating test_ema: {bars.Close}")  
print("Test EMA values:")
for i in range(len(test_ema.values)):
    print(f"EMA value at index {i}: {test_ema[i]}")
strategy.Create()

# Running the strategy with the PlayableBars
playable_bars.Play(strategy.CalcBar)