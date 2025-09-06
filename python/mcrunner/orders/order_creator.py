from typing import Callable
from .enums import SOrderParameters
from .market_order import MarketOrder
from .limit_order import LimitOrder
from .stop_order import StopOrder
from .stop_limit_order import StopLimitOrder
from .order_info import OrderInfo

class OrderCreator:
    def __init__(self):
        self.order_sent: Callable[[OrderInfo], None] | None = None

    def _wire(self, order):
        if self.order_sent:
            order.subscribe(self.order_sent)
        return order

    def limit(self, order_params: SOrderParameters):
        return self._wire(LimitOrder(order_params, True))

    def market_next_bar(self, order_params: SOrderParameters):
        return self._wire(MarketOrder(order_params, True))

    def market_this_bar(self, order_params: SOrderParameters):
        return self._wire(MarketOrder(order_params, False))

    def stop(self, order_params: SOrderParameters):
        return self._wire(StopOrder(order_params, True))

    def stop_limit(self, order_params: SOrderParameters):
        return self._wire(StopLimitOrder(order_params, True))
