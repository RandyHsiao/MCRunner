from dataclasses import dataclass
from ..orders.enums import EOrderAction

@dataclass
class ExecutedTrade:
    bar_index: int
    action: EOrderAction
    price: float
    size: float
