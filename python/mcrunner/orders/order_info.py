from dataclasses import dataclass, field
from .enums import EOrderAction, OrderExit

@dataclass
class OrderInfo:
    ConditionPrice: float = 0.0
    Price: float = 0.0
    Size: float = 0.0
    OrderAction: EOrderAction = EOrderAction.Buy
    Order: "BaseOrder" = None
    OrderExit: OrderExit = field(default_factory=OrderExit)
