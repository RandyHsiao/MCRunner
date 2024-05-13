#這段代碼是在模仿Multicharts.Net的功能，嘗試實現一個簡單的交易策略
#請協助我檢查這段代碼的可行性，以及是否有更好的實現方式
from abc import ABC, abstractmethod
from enum import Enum
import pandas as pd
import numpy as np
import cloudpickle
from collections import deque
import sys
from typing import List, Any

class ConsoleOutput:
    def clear(self):
        sys.stderr.write("\x1b[2J\x1b[H")

    def write(self, format, *args):
        print(format % args, end='')

    def write_line(self, format, *args):
        print(format % args)

# 載入市場數據
csv_path = 'C:\\Users\\Randy-P14s\\Documents\\Python\\pyneurgen_\\mnt\\data\\2330 1 Day.csv'
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()  # 移除列名中的空白

# 將列轉換成 NumPy 數組
prices_open = df['<Open>'].to_numpy()
prices_high = df['<High>'].to_numpy()
prices_low = df['<Low>'].to_numpy()
prices_close = df['<Close>'].to_numpy()
dates = pd.to_datetime(df['<Date>']).to_numpy()


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

class Bars:
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

class PlayableBars(Bars):
    def __init__(self, bars_to_play: List[Bar]):
        super().__init__()
        self.bars_to_play = bars_to_play

    def play(self, action):
        self._bars.clear()
        for bar in self.bars_to_play:
            self._bars.append(bar)
            action(bar)
        self.bars_to_play = None



# 創建 Bar 對象並添加到 Bars 對象中
bars = Bars()
for i in range(len(dates)):
    bar = Bar(dates[i], prices_high[i], prices_low[i], prices_open[i], prices_close[i], 0) # 假設 volume 為 0
    bars.add_bar(bar)

# 使用 BarSeries 對象訪問數據
print("最新的收盤價:", bars.close.value)
print("從最新的柱狀數據中往前推一個柱狀數據的收盤價:", bars.close[1])


# 定義市場數據字典
market_data = {
    'open': prices_open,
    'high': prices_high,
    'low': prices_low,
    'close': prices_close,
    'dates': dates
}

# 加載條件評估
with open('C:\\Users\\Randy-P14s\\Documents\\Python\\pyneurgen_\\mnt\\data\\specific_condition_evaluation.pkl', 'rb') as file:
    test_condition_evaluation = cloudpickle.load(file)

def set_exit_on_close(market_data, i, market_position):
    if market_position == 1 and pd.Timestamp(market_data['dates'][i]).weekday() == 4:
        return True
    return False

# 定義進出場條件函數
def entry_condition(market_data, index, boolean_array):
    return boolean_array[index]

def exit_condition(market_data, index):
    # 假設出場條件為 False
    return False

def entry_price_func(market_data, index, order_type="market"):
    if order_type == "market":
        # 市價單的進場價格是下一個交易日的開盤價
        return market_data['open'][index + 1]
    else:
        # 其他訂單類型的處理邏輯
        return market_data['close'][index] * 1.01  # 前一天收盤價的 1% 增加

class IOrderObject(ABC):
    @property
    @abstractmethod
    def ID(self):
        pass

    @property
    @abstractmethod
    def Info(self):
        pass

class IOrderMarket(IOrderObject):
    @abstractmethod
    def Send(self, numLots=None):
        pass

class OrderExit:
    FROM_ALL = 1
    TOTAL = 2
    FROM_ENTRY = 3
    pass

# # OrderExit 和 EOrderAction 枚舉（假設已根據提供的 Python 代碼定義）
# class OrderExit:
#     EExitType = Enum('EExitType', 'All Other')

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

class Order:
    def __init__(self, name, action, category, lots, openNext, exitTypeInfo):
        self.Name = name
        self.Action = action
        self.Category = category
        self.Lots = lots
        self.openNext = openNext
        self.ExitTypeInfo = exitTypeInfo
    def __str__(self):
        return f"Order: {self._orderParams.Action}, {self._orderParams.Lots}, {self._orderParams.Name}"        

class OrderInfo:
    def __init__(self, Order=None, OrderAction=None, OrderExit=None, Size=0.0, ConditionPrice=0.0, Price=0.0):
        if OrderAction is None:
            raise ValueError("OrderAction cannot be None")
        self.ConditionPrice = ConditionPrice
        self.Price = Price
        self.Size = Size
        self.OrderAction = OrderAction
        self.Order = Order
        self.OrderExit = OrderExit

class Orders:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def get_order(self, criteria):
        # Example: Retrieve orders based on a certain criteria
        return [order for order in self.orders if criteria(order)]

    def update_order_status(self, order_id, new_status):
        # Example: Update the status of a specific order
        for order in self.orders:
            if order.id == order_id:
                order.status = new_status

    def list_all_orders(self):
        return self.orders

class SOrderParameters:
    def __init__(self, action=None, lots=None, name=None, exitTypeInfo=None):
        if action is None:
            raise ValueError("Action parameter is required")
        if lots is None:
            lots = Contracts.Default()
        if name is None:
            name = ""

        self.action = action
        self.lots = lots
        self.name = name
        self.exitTypeInfo = exitTypeInfo

    @property
    def Lots(self):
        return self.lots

    @property
    def Action(self):
        return self.action

    @property
    def Name(self):
        return self.name

    @property
    def ExitTypeInfo(self):
        return self.exitTypeInfo

class IOrderCreator(ABC):
    @abstractmethod
    def Limit(self, order_params):
        pass

    @abstractmethod
    def MarketNextBar(self, order_params):
        pass

    @abstractmethod
    def MarketThisBar(self, order_params):
        pass

    @abstractmethod
    def Stop(self, order_params):
        pass

    @abstractmethod
    def StopLimit(self, order_params):
        pass

class IOrderManaged(ABC):
    @abstractmethod
    def set_order_sent_callback(self, callback):
        pass


class BaseOrder(ABC):
    def __init__(self, orderParams, orderCategory, openNext):
        self._orderParams = orderParams
        self._info = self._createOrderInfo(orderParams, orderCategory, openNext)
        self._id = self.__hash__()
        self.OrderSent = None 

    def _createOrderInfo(self, orderParams, orderCategory, openNext):
        return Order(
            name=orderParams.name,
            action=orderParams.action,
            category=orderCategory,
            lots=orderParams.Lots,
            openNext=openNext,
            exitTypeInfo=orderParams.ExitTypeInfo
        )        
 
    @property
    def ID(self):
        return self._id

    @property
    def Info(self):
        return self._info

    def setOrderSentCallback(self, callback):
        self.OrderSent = callback

    def TriggerOrderSent(self, orderInfo):
        if self.OrderSent is not None:
            self.OrderSent(orderInfo)

    def __eq__(self, other):
        if isinstance(other, BaseOrder):
            return all([
                self.OrderParams.Name == other.OrderParams.Name,
                self.OrderParams.Action == other.OrderParams.Action,
                self.OrderParams.ExitTypeInfo == other.OrderParams.ExitTypeInfo,
                self.OrderParams.Lots.Contract == other.OrderParams.Lots.Contract,
                self.OrderParams.Lots.Type == other.OrderParams.Lots.Type,
                self.Info.Category == other.Info.Category,
                self.Info.OnClose == other.Info.OnClose
            ])
        return False

    def __hash__(self):
        return hash((self._orderParams, self.Info.Category))

    @abstractmethod
    def Send(self, numLots):
        pass


class BaseOrder:
    def __init__(self, order_params: SOrderParameters, order_category: int, open_next: bool):
        self.order_params = order_params
        self.info = Order(order_params.name, order_params.action, order_category, order_params.lots, open_next, order_params.exit_type_info)
        self.id = hash((order_params, order_category, open_next))

    def __eq__(self, other):
        if not isinstance(other, BaseOrder):
            return False
        return (self.order_params == other.order_params and
                self.info.category == other.info.category and
                self.info.on_close == other.info.on_close)

    def __hash__(self):
        return hash((self.order_params, self.info.category, self.info.on_close))

    def trigger_order_sent(self, order_info):
        # 在這裡實現替代事件驅動模式的邏輯，例如通過直接調用或回調函數
        pass

class MarketOrder(BaseOrder, IOrderMarket):
    def __init__(self, orderParams, openNext=False):
        super().__init__(orderParams, OrderCategory.Market, openNext)

    def Send(self, numLots=None, new_name=None):
        if numLots is not None:
            if numLots < 0:
                raise ValueError("numLots must be larger than 0")
            else:
                order_info = OrderInfo(self, self._orderParams.Action, self._orderParams.ExitTypeInfo, self._orderParams.Lots.GetSize(numLots))
                self.TriggerOrderSent(order_info)
                self._info = order_info
        else:
            order_info = OrderInfo(self, self._orderParams.Action, self._orderParams.ExitTypeInfo, self._orderParams.Lots.GetSize())
            self.TriggerOrderSent(order_info)
            self._info = order_info

        if new_name is not None:
            raise NotImplementedError

    def SendFromEntry(self, numLots=None, new_name=None, fromName=None):
        if numLots is not None or new_name is not None or fromName is not None:
            raise NotImplementedError
        else:
            self.Send()

    def __str__(self):
        return f"MarketOrder: {self._orderParams.Action}, {self._orderParams.Lots}, {self._orderParams.Name}"

class OrderCreator(IOrderCreator, IOrderManaged):
    def __init__(self):
        self.OrderSent = []

    def register_OrderSent(self, callback):
        self.OrderSent.append(callback)

    def Limit(self, orderParams):
        # Implement the Limit order creation logic here
        pass

    def Stop(self, orderParams):
        # Implement the Stop order creation logic here
        pass

    def StopLimit(self, orderParams):
        # Implement the StopLimit order creation logic here
        pass

    def set_order_sent_callback(self, callback):
        self.OrderSent.append(callback)
        
    def MarketNextBar(self, orderParams):
        order = MarketOrder(orderParams, True)
        for callback in self.OrderSent:
            callback(order)
        return order

    def MarketThisBar(self, orderParams):
        order = MarketOrder(orderParams, False)
        for callback in self.OrderSent:
            callback(order)
        return order

    def OnOrderSent(self, order):
        for callback in self.OrderSent:
            callback(order)

    
class OrderManager:
    def __init__(self):
        self.entry_orders = deque()  # 使用deque來實現一個FIFO的隊列

    def add_entry_order(self, orderParams, orderType):
        if orderType == 'MarketNextBar':
            order = OrderCreator.MarketNextBar(orderParams)
        elif orderType == 'MarketThisBar':
            order = OrderCreator.MarketThisBar(orderParams)
        elif orderType == 'Limit':
            order = OrderCreator.Limit(orderParams)
        elif orderType == 'Stop':
            order = OrderCreator.Stop(orderParams)
        self.entry_orders.append(order)

    def match_exit_order(self, exit_order):
        if self.entry_orders:
            matched_entry_order = self.entry_orders.popleft()  # 移除並返回最早的進場訂單
            # 在這裡可以實現將出場訂單與進場訂單匹配的邏輯
            # 例如計算盈虧、更新持倉狀態等
            return matched_entry_order
        else:
            # 沒有匹配的進場訂單，可能需要處理這種異常情況
            return None

    
class MarketPosition:
    def __init__(self):
        self.position = 0

    def update_position(self, action):
        if action == EOrderAction.BUY or action == EOrderAction.BuyToCover:
            self.position = 1  # 设置为多头状态
        elif action == EOrderAction.SELL or action == EOrderAction.SellShort:
            self.position = -1  # 设置为空头状态
        else:
            self.position = 0  # 设置为无仓位状态

    @property
    def Position(self):
        return self.position


    
class SetExitOnClose(IOrderMarket):
    def __init__(self, order_id, market_position, order_params):
        self.order_id = order_id
        self.market_position = market_position
        self.order_params = order_params

    def Send(self):
        if self.market_position.position == 1:  # 如果当前持有多头仓位
            print(f"Closing long position with {self.order_params.Lots} lots at {self.order_params.Price}")
            # 这里应该调用实际的平多仓命令
        elif self.market_position.position == -1:  # 如果当前持有空头仓位
            print(f"Closing short position with {self.order_params.Lots} lots at {self.order_params.Price}")
            # 这里应该调用实际的平空仓命令
            
class OrderMarketThisBar(IOrderMarket):
    def __init__(self, order_id, order_params):
        self.order_id = order_id
        self.order_params = order_params

    @property
    def ID(self):
        return self.order_id

    @property
    def Info(self):
        return self.order_params

    def Send(self, strategy_info, numLots=None):
        print(f"Sending Market Order for this bar with {numLots} lots")  # 實現這一條的市價訂單的發送
        if self.order_params.action == EOrderAction.BUY:
            strategy_info.market_position = 1
        elif self.order_params.action == EOrderAction.SELL:
            strategy_info.market_position = -1
        elif self.order_params.action in [EOrderAction.SELL, EOrderAction.BuyToCover]:
            strategy_info.market_position = 0

class OrderMarketNextBar(IOrderMarket):
    def __init__(self, order_id, order_params):
        self.order_id = order_id
        self.order_params = order_params

    @property
    def ID(self):
        return self.order_id

    @property
    def Info(self):
        return self.order_params

    def Send(self, strategy_info, numLots=None):
        print(f"Sending Market Order for next bar with {numLots} lots")  # 实现下一条的市价订单的发送
        # 更新市场位置
        if self.order_params.action == EOrderAction.BUY:
            strategy_info.market_position = 1
        elif self.order_params.action == EOrderAction.SELL:
            strategy_info.market_position = -1
        elif self.order_params.action in [EOrderAction.SELL, EOrderAction.BuyToCover]:
            strategy_info.market_position = 0

class InvalidOrderException(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidOperationException(Exception):
    def __init__(self, message):
        super().__init__(message)

class PositionInfo:
    def __init__(self, size):
        self.Size = size

class IPosition:
    @property
    def Size(self):
        raise NotImplementedError

    def ValidateOrder(self, order):
        raise NotImplementedError

    def UpdatePosition(self, order):
        raise NotImplementedError

class LongPosition(IPosition):
    def __init__(self):
        self.positions = []

    @property
    def Size(self):
        return sum(position.Size for position in self.positions)

    def ValidateOrder(self, orderInfo):
        if orderInfo.OrderAction == EOrderAction.Buy:
            pass
        elif orderInfo.OrderAction == EOrderAction.Sell:
            if not self.positions:
                raise InvalidOrderException("Can't close position before opening one!")
            if orderInfo.OrderExit.ExitType != OrderExit.EExitType.All:
                raise InvalidOrderException("Only OrderExit.EExitType.All is currently supported")
        else:
            raise InvalidOrderException("Long orders only!")

    def UpdatePosition(self, orderInfo):
        if orderInfo.OrderAction == EOrderAction.Buy:
            self.OpenPosition(orderInfo)
        elif orderInfo.OrderAction == EOrderAction.Sell:
            self.ClosePosition(orderInfo)
        else:
            raise ValueError(f"Unsupported OrderAction {orderInfo.OrderAction}")

    def OpenPosition(self, orderInfo):
        new_position = PositionInfo(size=orderInfo.Size)
        self.positions.append(new_position)

    def ClosePosition(self, orderInfo):
        if not self.positions:
            raise InvalidOperationException("Can't close position before opening one!")
        if orderInfo.OrderExit.ExitType == OrderExit.EExitType.All:
            self.positions.clear()
        else:
            raise NotImplementedError("Other OrderExit types not currently supported")


class ShortPosition(IPosition):
    def __init__(self):
        self.positions = []

    @property
    def Size(self):
        return sum(position.Size for position in self.positions)

    def ValidateOrder(self, orderInfo):
        if orderInfo.OrderAction == EOrderAction.SellShort:
            pass
        elif orderInfo.OrderAction == EOrderAction.BuyToCover:
            if not self.positions:
                raise InvalidOrderException("Can't close position before opening one!")
            if orderInfo.OrderExit.ExitType != OrderExit.EExitType.All:
                raise InvalidOrderException("Only OrderExit.EExitType.All is currently supported")
        else:
            raise InvalidOrderException("Short orders only!")

    def UpdatePosition(self, orderInfo):
        if orderInfo.OrderAction == EOrderAction.SellShort:
            self.OpenPosition(orderInfo)
        elif orderInfo.OrderAction == EOrderAction.BuyToCover:
            self.ClosePosition(orderInfo)
        else:
            raise ValueError(f"Unsupported OrderAction {orderInfo.OrderAction}")

    def OpenPosition(self, orderInfo):
        new_position = PositionInfo(size=orderInfo.Size)
        self.positions.append(new_position)

    def ClosePosition(self, orderInfo):
        if not self.positions:
            raise InvalidOperationException("Can't close position before opening one!")
        if orderInfo.OrderExit.ExitType == OrderExit.EExitType.All:
            self.positions.clear()
        else:
            raise NotImplementedError("Other OrderExit types not currently supported")


class StrategyPerformance:
    def __init__(self):
        self.avg_entry_price = 0.0
        self.open_equity = 0.0
        self.closed_equity = 0.0
        self.market_position = 0
        self.market_position_at_broker = 0
        self.avg_entry_price_at_broker = 0.0
        self.avg_entry_price_at_broker_for_the_strategy = 0.0
        self.signals = []

    def update_market_position_at_broker(self, position_change: float):
            self.market_position_at_broker += position_change

class StrategyRunner:
    def __init__(self, strategy, bars, strategy_info=None):
        self.strategy = strategy
        self.bars = bars
        self.strategy_info = strategy_info if strategy_info else StrategyPerformance()

    def run(self):
        # 假设策略有初始化和开始计算的方法
        if hasattr(self.strategy, 'prepare'):
            self.strategy.prepare()
        if hasattr(self.strategy, 'start_calc'):
            self.strategy.start_calc()

        for bar in self.bars:
            # 假设策略有处理bar的方法
            self.strategy.calc_bar(bar)

class StrategyBacktester:
    def __init__(self, strategy_class, bars):
        self.strategy = strategy_class()  # 直接实例化策略
        self.bars = bars
        self.strategy_info = StrategyPerformance()
        self.runner = StrategyRunner(self.strategy, self.bars, self.strategy_info)

    def backtest(self, action=None):
        self.runner.run()
        if action:
            for bar in self.bars:
                action(bar)

class PlayableBars:
    def __init__(self, bars):
        self.bars = bars

    def play(self, action):
        for bar in self.bars:
            action(bar)




class Strategy:
    def __init__(self, entry_condition, exit_condition, order_manager):
        self.entry_condition = entry_condition
        self.exit_condition = exit_condition
        self.order_creator = OrderCreator()
        self.order_manager = order_manager
        self.MarketPosition = 0  # Add MarketPosition as an attribute

    def should_enter(self, market_data, index, boolean_array):
        # Include MarketPosition in the condition
        return self.MarketPosition == 0 and self.entry_condition(market_data, index, boolean_array)

    def should_exit(self, market_data, index):
        # Include MarketPosition in the condition
        return self.MarketPosition != 0 and self.exit_condition(market_data, index)
    
    def send_order(self, order):
        self.order_manager.add_order(order)

    def update_market_position(self, position_change):
        self.MarketPosition += position_change




class StrategyBacktester:
    def __init__(self, strategy_class, bars, min_index_for_entry, market_data, boolean_array):
        self.order_creator = OrderCreator()  # 負責創建訂單
        self.strategy_manager = StrategyManager(self.order_creator)  # 管理策略運行和性能信息
        self.strategy_info = self.strategy_manager.strategy_info  # 策略性能信息
        self.playable_bars = bars  # 市場數據
        # 初始化策略實例，將額外的參數傳遞給策略類
        self.strategy = strategy_class(
            strategy_info=self.strategy_info, 
            order_creator=self.order_creator, 
            min_index_for_entry=min_index_for_entry, 
            market_data=market_data, 
            boolean_array=boolean_array
        )
        # 可能不再需要StrategyRunner，除非它在策略運行中提供了特定功能
        # 如果StrategyRunner提供了核心的運行機制，則應該保留
        # self.strategy_runner = StrategyRunner(self.strategy, self.playable_bars, self.order_creator)

    def Backtest(self):
        total_profit = 0

        # for bar in self.playable_bars:
        #             # 更新策略狀態或進行計算
        #             self.strategy.calculate(bar)

        for i in range(len(self.market_data['dates']) - 1):
            if i < self.min_index_for_entry:
                continue

            # Check entry condition
            if self.strategy.should_enter(self.market_data, i, self.boolean_array):
                # Logic to handle entry
                print(f"Entering market at index {i}")
                # Create and store entry order
                buyOrderParams = SOrderParameters(EOrderAction.Buy, Lots(Contracts.Default()), 'EnMarket-B')
                buyMarketOrder = self.strategy.order_creator.MarketNextBar(buyOrderParams)
                self.strategy.send_order(buyMarketOrder)
                self.strategy.order_manager.append(buyMarketOrder)

            # Check exit condition
            if self.strategy.should_exit(self.market_data, i):
                # Logic to handle exit
                print(f"Exiting market at index {i}")
                # Create and store exit order
                sellOrderParams = SOrderParameters(EOrderAction.Sell, Lots(Contracts.Default()), 'ExMarket-S')
                sellMarketOrder = self.strategy.order_creator.MarketNextBar(sellOrderParams)
                self.strategy.send_order(sellMarketOrder)
                self.strategy.order_manager.append(sellMarketOrder)

        # Here, additional logic can be added to calculate and return performance metrics
        print(f"Total orders: {len(self.strategy.order_manager)}")
    
    @property
    def Strategy(self):
        return self.strategy

    @property
    def StrategyInfo(self):
        return self.strategy_info

# Assume 'market_data' is a dictionary containing market data
strategy = Strategy(entry_condition, exit_condition, OrderCreator, OrderManager)
backtester = StrategyBacktester(strategy, market_data, boolean_array=test_condition_evaluation, min_index_for_entry=10)
backtester.Backtest()