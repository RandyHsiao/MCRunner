from typing import List
from ..orders import OrderInfo, EOrderAction, OrderExit, EExitType
from .position_info import PositionInfo

class InvalidOrderException(Exception):
    pass

class LongPosition:
    def __init__(self):
        self.positions: List[PositionInfo] = []

    @property
    def Size(self):
        return sum(p.Size for p in self.positions)

    def validate_order(self, order: OrderInfo):
        if order.OrderAction == EOrderAction.Buy:
            return
        if order.OrderAction == EOrderAction.Sell:
            if not self.positions:
                raise InvalidOrderException("Can't close position before opening one!")
            if order.OrderExit.ExitType != EExitType.All:
                pass
        else:
            raise InvalidOrderException("Long orders only!")

    def update_position(self, order: OrderInfo):
        if order.OrderAction == EOrderAction.Buy:
            self.positions.append(PositionInfo(order.Size))
        elif order.OrderAction == EOrderAction.Sell:
            self.positions.clear()
        else:
            raise InvalidOrderException("Unsupported OrderAction")
