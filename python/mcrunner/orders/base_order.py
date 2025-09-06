from typing import Callable, List
from .enums import SOrderParameters, OrderCategory
from .order_info import OrderInfo

class BaseOrder:
    def __init__(self, order_params: SOrderParameters, category: OrderCategory, open_next: bool):
        self.OrderParams = order_params
        self.Category = category
        self.OpenNext = open_next
        self.callbacks: List[Callable[[OrderInfo], None]] = []

    def subscribe(self, cb: Callable[[OrderInfo], None]):
        self.callbacks.append(cb)

    def _trigger(self, info: OrderInfo):
        for cb in list(self.callbacks):
            cb(info)
