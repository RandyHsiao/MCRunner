# import pandas as pd
import numpy as np
from typing import TypeVar, Generic, Any, List
from abc import ABC, abstractmethod
from enum import Enum
import inspect
from datetime import datetime, timedelta

T = TypeVar('T')

# csv_path = 'C:\\Users\\Randy-P14s\\Documents\\Python\\pyneurgen_\\mnt\\data\\2330 1 Day.csv'
# df = pd.read_csv(csv_path)
# df.columns = df.columns.str.strip()  # 移除列名中的空白

# # 將列轉換成 NumPy 數組
# prices_open = df['<Open>'].to_numpy()
# prices_high = df['<High>'].to_numpy()
# prices_low = df['<Low>'].to_numpy()
# prices_close = df['<Close>'].to_numpy()
# dates = pd.to_datetime(df['<Date>']).to_numpy()

# 創建模擬數據
dates = [datetime.now() - timedelta(days=i) for i in range(10)]
prices_open = np.array([100, 101, 102, 103, 104, 105, 106, 107, 108, 109])
prices_high = np.array([105, 106, 107, 108, 109, 110, 111, 112, 113, 114])
prices_low = np.array([95, 96, 97, 98, 99, 100, 101, 102, 103, 104])
prices_close = np.array([102, 103, 104, 105, 106, 107, 108, 109, 110, 111])
volumes = np.array([1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009])
    
# ================================================================
# 定義 Bar 和 BarSeries 類
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
    def HighValue(self):
        return self._bars[self.CurrentBar].high

    @property
    def LowValue(self):
        return self._bars[self.CurrentBar].low

    @property
    def OpenValue(self):
        return self._bars[self.CurrentBar].open

    @property
    def CloseValue(self):
        return self._bars[self.CurrentBar].close

    @property
    def VolumeValue(self):
        return self._bars[self.CurrentBar].volume

    @property
    def TimeValue(self):
        return self._bars[self.CurrentBar].time

    @property
    def LastBarTime(self):
        last_bar = self.CurrentBar - 1
        if last_bar < 0:
            raise IndexError()
        return self._bars[last_bar].time

    @property
    def Time(self):
        return BarSeries(self, "Time")

    @property
    def High(self):
        return BarSeries(self, "High")

    @property
    def Low(self):
        return BarSeries(self, "Low")

    @property
    def Open(self):
        return BarSeries(self, "Open")

    @property
    def Close(self):
        return BarSeries(self, "Close")

    @property
    def Volume(self):
        return BarSeries(self, "Volume")

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
        bar = self.bars.Bars[index]  # Directly access the _bars list using the calculated index
        # print(f"Accessing {self.field_name} from bar at index {index}")  # 添加这行调试输出
        return self._get_field(bar)

    def __len__(self):
        return len(self.bars.Bars)  # 添加这个方法
    
    @property
    def value(self):
        return self[0]

    def Lowest(self, lookback_period, bars_ago=0):
        values = [self[i] for i in range(bars_ago, bars_ago + lookback_period)]
        return min(values) if values else None

    def Highest(self, lookback_period, bars_ago=0):
        values = [self[i] for i in range(bars_ago, bars_ago + lookback_period)]
        return max(values) if values else None
    
    # def Lowest(self, lookback_period, bars_ago=0):
    #     current_bar = self.bars.CurrentBar
    #     start_index = current_bar - lookback_period - bars_ago + 1
    #     end_index = current_bar - bars_ago + 1

    #     if start_index < 0 or end_index > current_bar + 1:
    #         raise IndexError(f"Lookback period ({lookback_period}) and bars ago ({bars_ago}) are too large for the current bar count ({current_bar + 1})")

    #     values = [self._get_field(bar) for bar in self.bars[start_index:end_index]]
    #     return min(values) if values else None

    # def Highest(self, lookback_period, bars_ago=0):
    #     current_bar = self.bars.CurrentBar
    #     start_index = current_bar - lookback_period - bars_ago + 1
    #     end_index = current_bar - bars_ago + 1

    #     if start_index < 0 or end_index > current_bar + 1:
    #         raise IndexError(f"Lookback period ({lookback_period}) and bars ago ({bars_ago}) are too large for the current bar count ({current_bar + 1})")

    #     values = [self._get_field(bar) for bar in self.bars[start_index:end_index]]
    #     return max(values) if values else None

    # def Lowest(self, lookback_period, bars_ago=1):
    #     # 计算最低值
    #     values = [bar.Low for bar in self.bars[-(lookback_period + bars_ago):-bars_ago]]
    #     return min(values) if values else None

    # def Highest(self, lookback_period, bars_ago=1):
    #     # 计算最高值
    #     values = [bar.High for bar in self.bars[-(lookback_period + bars_ago):-bars_ago]]
    #     return max(values) if values else None
    
    # def LowestSeries(self, lookback_period: int, bars_ago: int):
    #     if bars_ago < 0:
    #         raise IndexError("不能往未來看！")

    #     count = len(self.Value)
    #     index = count - 1 - bars_ago

    #     if index < 0:
    #         raise IndexError(f"{index} 太遠了！目前只有 {count} 個條")

    #     # 計算回溯期間內的最低值
    #     lowest_values = [min(self.values[i - lookback_period + 1:i + 1]) for i in range(index, -1, -1)]
    #     return lowest_values

    
    # def HighestSeries(self, lookback_period: int, bars_ago: int):
    #     if bars_ago < 0:
    #         raise IndexError("不能往未來看！")

    #     count = len(self.Value)
    #     index = count - 1 - bars_ago

    #     if index < 0:
    #         raise IndexError(f"{index} 太遠了！目前只有 {count} 個條")

    #     # 計算回溯期間內的最高值
    #     highest_values = [max(self.values[i - lookback_period + 1:i + 1]) for i in range(index, -1, -1)]
    #     return highest_values


# class PlayableBars(Bars):
#     def __init__(self, barsToPlay: List[Bar]):
#         super().__init__()
#         self.BarsToPlay = barsToPlay

#     def Play(self, action):
#         self._bars.clear()
#         self._current_bar = -1   
                
#         for i, bar in enumerate(self.BarsToPlay):
#             self.AddBar(bar)  # 使用 AddBar 确保正确更新 CurrentBar
#             print(f"Playing Bar {i + 1}: CurrentBar = {self._current_bar}, Close = {bar.Close}")  # 打印当前Bar信息
#             action(bar)
class PlayableBars(Bars):
    def __init__(self, barsToPlay: List[Bar]):
        super().__init__()
        self.BarsToPlay = barsToPlay
        for bar in barsToPlay:
            self.AddBar(bar)  # 将 barsToPlay 中的 Bar 对象添加到 self._bars 中

    def Play(self, action):
        for i, bar in enumerate(self.Bars):
            # print(f"Playing Bar {i + 1}: CurrentBar = {self._current_bar}, Close = {bar.Close}")  # 打印当前Bar信息
            action(bar)

# class PlayableBars(Bars):
#     def __init__(self, barsToPlay: List[Bar]):
#         super().__init__()
#         self.BarsToPlay = barsToPlay

#     def Play(self, action):
#         self._bars.clear()
#         self._current_bar = -1   
             
#         for bar in self.BarsToPlay:
#             self.AddBar(bar)
#             action() 

# 創建 Bar 對象並添加到 Bars 對象中
bars = Bars()
for i in range(len(dates)):
    bar = Bar(dates[i], prices_high[i], prices_low[i], prices_open[i], prices_close[i], volumes[i])
    bars.AddBar(bar)

class XAverage:
    def __init__(self, price_series, length):
        self.values = []
        self.Length = length
        self.Price = price_series
        self.StartCalc()
    
    def Create(self):
        pass

    def StartCalc(self):
        print("StartCalc method called")  # 添加这个打印语句
        if isinstance(self.Price, BarSeries):
            price_data = [self.Price[i] for i in range(len(self.Price.bars.Bars))]
            # print(f"Price data from BarSeries: {price_data}")
        else:
            price_data = self.Price
            # print(f"Price data: {price_data}")

        if len(price_data) < self.Length:
            return

        alpha = 2.0 / (self.Length + 1)

        self.values.append(price_data[0])
        for i in range(1, len(price_data)):
            self.values.append(self.values[-1] + alpha * (price_data[i] - self.values[-1]))

    def Caclbar(self):
        pass

    def __getitem__(self, bars_ago: int) -> float:
        if bars_ago < 0 or bars_ago >= len(self.values):
            raise IndexError("Index out of range")
        return self.values[bars_ago]

    @property
    def Value(self) -> float:
        return self.values[-1] if self.values else None



# ema = XAverage(bars.Close, 50)


# lowest_Close = bars.Close.Lowest(10, 1)
# highest_Close = bars.Close.Highest(10, 1)
    
# 测试 BarSeries 类的 Lowest 和 Highest 方法
# bar_series = BarSeries(bars.Bars)
# lowest_Close = bars.Close.Lowest(10, 1)
# highest_Close = bars.Close.Highest(10, 1)

# lowest_Close, highest_Close

# ================================================================
class EOrderAction(Enum):
    Buy = 1
    Sell = 2
    SellShort = 3
    BuyToCover = 4

class OrderCategory(Enum):
    Market = 1
    Limit = 2
    Stop = 3
    StopLimit = 4

class Lots:
    def __init__(self, num):
        self.num = num

    def GetSize(self, numLots=None):
        if numLots is not None:
            if numLots == 0:
                return Contracts.Default().num  # return default Lots value when numLots is 0
            else:
                return numLots
        else:
            return self.num

    def __str__(self):
        return f"Lots(num={self.num})"


class Contracts:
    @staticmethod
    def Default():
        return Lots(1)

    @staticmethod
    def CreateUserSpecified(num):
        return Lots(num)
    
class SOrderParameters:
    def __init__(self, lots=None, action=None, exit_type_info=None, name=None):
        if action is None:
            raise ValueError("Action parameter is required")
        if lots is None:
            lots = Contracts.Default()
        if name is None:
            name = ""        
            
        self._lots = lots
        self._action = action
        self._exit_type_info = exit_type_info
        self._name = name

    @property
    def Lots(self):
        return self._lots

    @Lots.setter
    def Lots(self, lots):
        self._lots = lots

    @property
    def Action(self):
        return self._action

    @Action.setter
    def Action(self, action):
        self._action = action

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, name):
        self._name = name

    @property
    def ExitTypeInfo(self):
        return self._exit_type_info

    @ExitTypeInfo.setter
    def ExitTypeInfo(self, exit_type_info):
        self._exit_type_info = exit_type_info
    
class OrderInfo:
    def __init__(self):
        self.ConditionPrice = None
        self.Price = None
        self.Size = None
        self.OrderAction = None
        self.Order = None
        self.OrderExit = None

class Order:
    def __init__(self, name, action, category, lots, open_next, exit_type_info):
        self.Name = name
        self.Action = action
        self.Category = category
        self.Lots = lots
        self.OpenNext = open_next
        self.ExitTypeInfo = exit_type_info

class BaseOrder:
    def __init__(self, order_params, order_category, open_next):
        self.OrderParams = order_params
        self.Info = Order(
            order_params.Name,
            order_params.Action,
            order_category,
            order_params.Lots,
            open_next,
            order_params.ExitTypeInfo
        )
        self.ID = self.GetHashCode()

    def Equals(self, obj):
        equals = False
        if obj is not None and isinstance(obj, BaseOrder):
            order = obj
            if (order.OrderParams.Name == self.OrderParams.Name
                and order.OrderParams.Action == self.OrderParams.Action
                and order.OrderParams.ExitTypeInfo == self.OrderParams.ExitTypeInfo
                and order.OrderParams.Lots.Contract == self.OrderParams.Lots.Contract
                and order.OrderParams.Lots.Type == self.OrderParams.Lots.Type
                and order.Info.Category == self.Info.Category
                and order.Info.OnClose == self.Info.OnClose):
                equals = True
        return equals

    def GetHashCode(self):
        # return hash((self.OrderParams, self.Info.Category, self.Info.OnClose))
        return hash((self.OrderParams, self.Info.Category))
    
    def TriggerOrderSent(self, order_info):
        # 在Python中，我們不會使用事件驅動，所以這個方法可能不會被使用。
        pass


class MarketOrder(BaseOrder):
    def __init__(self, order_params, open_next=False):
        super().__init__(order_params, OrderCategory.Market, open_next)

    def Send(self, num_lots=None):
        if num_lots is not None and num_lots < 0:
            raise ValueError("num_lots must be larger than 0")
        elif num_lots == 0:
            self.Send()
        else:
            order_info = OrderInfo()
            order_info.Order = self
            order_info.OrderAction = self.OrderParams.Action
            order_info.OrderExit = self.OrderParams.ExitTypeInfo
            order_info.Size = self.OrderParams.Lots.GetSize(num_lots)
            self.TriggerOrderSent(order_info)

    def SendFromEntry(self, num_lots=None, from_name=None):
        raise NotImplementedError("SendFromEntry method is not implemented")

class OrderCreator:
    def __init__(self):
        self.OrderSentCallbacks = []

    def Limit(self, order_params):
        # order = LimitOrder(order_params, True)
        # order.OrderSentCallbacks = self.OrderSentCallbacks
        # return order
        pass

    def MarketNextBar(self, order_params):
        order = MarketOrder(order_params, True)
        order.OrderSentCallbacks = self.OrderSentCallbacks
        for callback in order.OrderSentCallbacks:
            callback(order)
        return order

    @staticmethod
    def MarketThisBar(self, order_params):
        order = MarketOrder(order_params, False)
        order.OrderSentCallbacks = self.OrderSentCallbacks
        for callback in order.OrderSentCallbacks:
            callback(order)
        return order

    def Stop(self, order_params):
        # order = StopOrder(order_params, True)
        # order.OrderSentCallbacks = self.OrderSentCallbacks
        # for callback in order.OrderSentCallbacks:
        #     callback(order)
        # return order
        pass

    def StopLimit(self, order_params):
        # order = StopLimitOrder(order_params, True)
        # order.OrderSentCallbacks = self.OrderSentCallbacks
        # for callback in order.OrderSentCallbacks:
        #     callback(order)
        # return order
        pass

    def AddOrderSentCallback(self, callback):
        self.OrderSentCallbacks.append(callback)

class StrategyPerformance:
    def __init__(self):
        self.avg_entry_price = 0.0
        self.open_equity = 0.0
        self.closed_equity = 0.0
        self.MarketPosition = 0
        self.market_position_at_broker = 0
        self.avg_entry_price_at_broker = 0.0
        self.avg_entry_price_at_broker_for_the_strategy = 0.0
        self.signals = []

    def update_market_position_at_broker(self, position_change: float):
            self.market_position_at_broker += position_change

class CStudyAbstract:
    def __init__(self, bars):
        self.bars = bars

    def Create(self):
        pass

    def StartCalc(self):
        pass

    def CalcBar(self):
        pass


    
class PriceBreakouts(CStudyAbstract):
    def __init__(self, bars):
        super().__init__(bars)
        self.EMALength = 5
        self.LookbackPeriod = 3
        self.enterLong = None
        self.enterShort = None
        self.exitLong = None
        self.exitShort = None
        self.EMA = None
        self.lowestClose = None
        self.highestClose = None
        self.emaValues = None
        self.StrategyInfo = StrategyPerformance()

    def Create(self):
        # Assuming OrderCreator and VariableSeries are defined elsewhere
        order_creator = OrderCreator()
        self.enterLong = order_creator.MarketNextBar(SOrderParameters(Contracts.Default, EOrderAction.Buy, "EnMarket-L"))
        self.enterShort = order_creator.MarketNextBar(SOrderParameters(Contracts.Default, EOrderAction.SellShort, "EnMarket-S"))
        self.exitLong = order_creator.MarketNextBar(SOrderParameters(Contracts.Default, EOrderAction.Sell, "ExMarket-L"))
        self.exitShort = order_creator.MarketNextBar(SOrderParameters(Contracts.Default, EOrderAction.BuyToCover, "ExMarket-S"))
        
        if not self.bars or not hasattr(self.bars, 'Close'):
            raise ValueError("Bars object is required with a Close series available for EMA calculation.")
        else:
            print("Bars object received successfully for EMA calculation.")
            print(f"Type of self.bars.Close: {type(self.bars.Close)}")  # 添加这行代码
            print(f"Length of self.bars.Close: {len(self.bars.Close)}")  # 添加这行代码
        
        self.lowestClose = VariableSeries()
        self.highestClose = VariableSeries()
        self.emaValues = VariableSeries()

        self.EMA = XAverage(self.bars.Close, self.EMALength)
        print(f"EMA: {self.EMA.values}")

    def StartCalc(self):
        pass

    def CalcBar(self):
        # self.lowestClose.value = self.bars.Close.Lowest(self.LookbackPeriod, 1)
        # self.highestClose.value = self.bars.Close.Highest(self.LookbackPeriod, 1)
        # self.emaValues.value = self.EMA[0]
        if len(self.bars.Bars) < self.LookbackPeriod + 1 or len(self.EMA.values) == 0:
            return

        self.lowestClose.append(self.bars.Close.Lowest(self.LookbackPeriod, 1))
        self.highestClose.append(self.bars.Close.Highest(self.LookbackPeriod, 1))
        self.emaValues.append(self.EMA[0])

        current_bar = self.bars.CurrentBar
        print(f"Bar {current_bar + 1}:")
        print(f"Current Bar Close: {self.bars.Close[0]}, Previous Bar Close: {self.bars.Close[1]}")
        print(f"Lowest Close in Last {self.LookbackPeriod} Bars: {self.lowestClose[0]}")
        print(f"Highest Close in Last {self.LookbackPeriod} Bars: {self.highestClose[0]}")       
        print(f"Latest EMA Value: {self.emaValues.Value}")

        # self.emaValues.append(self.EMA[0])   

        # if len(self.bars.Bars) < 6:
        #     return
        
        # if self.StrategyInfo.MarketPosition == 0:
        #     if (self.bars.Close[0] > self.highestClose[0]) and (self.bars.Close[1] < self.highestClose[1]):
        #         self.enterLong.Send()
        #     elif (self.bars.Close[0] < self.lowestClose[0]) and (self.bars.Close[1] > self.lowestClose[1]):
        #         self.enterShort.Send()
        # elif self.StrategyInfo.MarketPosition > 0:
        #     if (self.bars.Close[0] < self.emaValues[0]) and (self.bars.Close[1] >= self.emaValues[1]):
        #         self.exitLong.Send()
        # elif self.StrategyInfo.MarketPosition < 0:
        #     if (self.bars.Close[0] > self.emaValues[0]) and (self.bars.Close[1] <= self.emaValues[1]):
        #         self.exitShort.Send()

# 創建 PlayableBars 對象
playable_bars = PlayableBars(bars.Bars)

# 創建策略對象
strategy = PriceBreakouts(playable_bars)
strategy.Create()

# 使用 PlayableBars 進行回測
playable_bars.Play(lambda bar: strategy.CalcBar())
#================================================================
# # 測試 PriceBreakouts 類
# print("\nTesting PriceBreakouts class:")
# print("=" * 30)

# # 創建 PriceBreakouts 實例
# strategy = PriceBreakouts(bars)
# strategy.Create()

# # 模擬調用 CalcBar 方法並在每次迭代時打印索引為 0 和 1 的值
# for i in range(len(bars.Bars)):
#     strategy.CalcBar()
    
#     print(f"Bar {i + 1}:")
#     print(f"Current Bar Close: {bars.Close[0]}, Previous Bar Close: {bars.Close[1] if i > 0 else 'N/A'}")
#     # print(f"Current highestClose: {strategy.highestClose[0]}, Previous highestClose: {strategy.highestClose[1] if i > 0 else 'N/A'}")
#     # print(f"Current lowestClose: {strategy.lowestClose[0]}, Previous lowestClose: {strategy.lowestClose[1] if i > 0 else 'N/A'}")
#     # print(f"Current EMA: {strategy.emaValues[0]}, Previous EMA: {strategy.emaValues[1] if i > 0 else 'N/A'}")
#     print("-" * 50)

