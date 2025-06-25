from typing import List, Callable
from ..orders import (
    OrderCreator,
    OrderInfo,
    EOrderAction,
    OrderCategory,
)
from ..positions import LongPosition, ShortPosition
from .strategy_performance import StrategyPerformance
from .trade import ExecutedTrade

class StrategyManager:
    def __init__(self, order_creator: OrderCreator):
        self._long = LongPosition()
        self._short = ShortPosition()
        self.StrategyInfo = StrategyPerformance()
        self.ExecutedOrders: List[ExecutedTrade] = []
        self._untriggered: List[OrderInfo] = []
        self._prev_submitted: List[OrderInfo] = []
        self.OrderValidated: List[Callable[[OrderInfo], None]] = []
        self.OrderCanceled: List[Callable[[OrderInfo], None]] = []
        order_creator.order_sent = self.on_order_sent

    def on_order_sent(self, order: OrderInfo):
        self.validate_order(order)
        if order not in self._untriggered:
            self._untriggered.append(order)
            for cb in self.OrderValidated:
                cb(order)

    def validate_order(self, order: OrderInfo):
        if order.OrderAction in (EOrderAction.Buy, EOrderAction.Sell):
            self._long.validate_order(order)
        else:
            self._short.validate_order(order)

    def trigger_orders(self, bar, index: int):
        triggered = []
        for order in list(self._untriggered):
            if order.Order.Category == OrderCategory.Market:
                triggered.append(order)
            elif order.Order.Category in (OrderCategory.Limit, OrderCategory.Stop, OrderCategory.StopLimit):
                price = order.ConditionPrice or order.Price
                if order.OrderAction in (EOrderAction.Buy, EOrderAction.BuyToCover):
                    if price >= getattr(bar, 'Low', 0):
                        triggered.append(order)
                else:
                    if price <= getattr(bar, 'High', 0):
                        triggered.append(order)
        for order in triggered:
            self.on_order_triggered(order, bar, index)

        for order in list(self._prev_submitted):
            if order not in self._untriggered:
                for cb in self.OrderCanceled:
                    cb(order)
        self._prev_submitted = self._untriggered
        self._untriggered = []

    def on_order_triggered(self, order: OrderInfo, bar, index: int):
        if order.Price <= 0:
            order.Price = getattr(bar, 'Close', 0)
        self.ExecutedOrders.append(ExecutedTrade(index, order.OrderAction, order.Price, order.Size))
        if order.OrderAction in (EOrderAction.Buy, EOrderAction.Sell):
            self._long.update_position(order)
        else:
            self._short.update_position(order)
        self.StrategyInfo.MarketPosition = int(self._long.Size - self._short.Size)
        if order in self._untriggered:
            self._untriggered.remove(order)
        if order in self._prev_submitted:
            self._prev_submitted.remove(order)
