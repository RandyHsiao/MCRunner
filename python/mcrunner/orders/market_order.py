from .enums import SOrderParameters, OrderCategory, EOrderAction
from .order_info import OrderInfo
from .base_order import BaseOrder

class MarketOrder(BaseOrder):
    def __init__(self, order_params: SOrderParameters, open_next: bool = False):
        super().__init__(order_params, OrderCategory.Market, open_next)

    def send(self, num_lots: int = 0):
        if num_lots < 0:
            raise ValueError("numLots must be >= 0")
        size = self.OrderParams.contracts.contract if not self.OrderParams.contracts.is_user_specified else num_lots or self.OrderParams.contracts.contract
        info = OrderInfo(
            Order=self,
            OrderAction=self.OrderParams.action,
            OrderExit=self.OrderParams.exit_type_info,
            Size=size
        )
        self._trigger(info)
