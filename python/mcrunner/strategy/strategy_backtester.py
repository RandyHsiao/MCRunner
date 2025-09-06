from typing import Iterable, Callable
from ..instruments import Bar, PlayableBars
from ..orders import OrderCreator, OrderInfo
from .strategy_runner import StrategyRunner
from .strategy_manager import StrategyManager
from .strategy_performance import StrategyPerformance

class StrategyBacktester:
    def __init__(self, strategy_cls, bars: Iterable[Bar]):
        self.order_creator = OrderCreator()
        self.manager = StrategyManager(self.order_creator)
        self.strategy_info = self.manager.StrategyInfo
        self.playable_bars = PlayableBars(bars)
        self.runner = StrategyRunner(strategy_cls,
                                     bars_data=self.playable_bars.to_single_data_stream(),
                                     order_creator=self.order_creator,
                                     strategy_info=self.strategy_info)
        self.Strategy = self.runner.Strategy

    def backtest(self, action: Callable[[Bar], None] | None = None):
        self.runner.create()
        self.runner.start_calc()
        def callback(bar):
            self.runner.calc_bar()
            index = self.runner.Strategy.Bars.CurrentBar
            self.manager.trigger_orders(bar, index)
            if action:
                action(bar)
        self.playable_bars.play(callback)
