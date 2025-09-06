from typing import Iterable
from ..instruments import Bars
from ..orders import OrderCreator
from .strategy_performance import StrategyPerformance

class StrategyRunner:
    def __init__(self, strategy_cls, bars_data: Iterable[Bars] = None,
                 order_creator: OrderCreator = None,
                 strategy_info: StrategyPerformance = None):
        self.Strategy = strategy_cls()
        self._bars = list(bars_data or [])
        self._order_creator = order_creator or OrderCreator()
        self._strategy_info = strategy_info or StrategyPerformance()
        # manager is expected to be handled by caller
        # supply strategy with required attributes
        self.Strategy.Bars = self._bars[0] if self._bars else Bars()
        self.Strategy.OrderCreator = self._order_creator
        self.Strategy.StrategyInfo = self._strategy_info

    def create(self):
        if hasattr(self.Strategy, 'create'):
            self.Strategy.create()

    def start_calc(self):
        if hasattr(self.Strategy, 'start_calc'):
            self.Strategy.start_calc()

    def calc_bar(self):
        if hasattr(self.Strategy, 'calc_bar'):
            self.Strategy.calc_bar()
