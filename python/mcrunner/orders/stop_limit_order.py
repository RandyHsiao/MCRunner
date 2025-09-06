from .enums import SOrderParameters, OrderCategory
from .order_info import OrderInfo
from .base_order import BaseOrder

class StopLimitOrder(BaseOrder):
    def __init__(self, order_params: SOrderParameters, open_next: bool = False):
        super().__init__(order_params, OrderCategory.StopLimit, open_next)

    def send(self, price: float, limit_price: float, num_lots: int = 0):
        if price <= 0 or limit_price <= 0:
            raise ValueError("price must be > 0")
        if num_lots < 0:
            raise ValueError("numLots must be >= 0")
        size = self.OrderParams.contracts.contract if not self.OrderParams.contracts.is_user_specified else num_lots or self.OrderParams.contracts.contract
        info = OrderInfo(
            ConditionPrice=price,
            Price=limit_price,
            Order=self,
            OrderAction=self.OrderParams.action,
            OrderExit=self.OrderParams.exit_type_info,
            Size=size,
        )
        self._trigger(info)
