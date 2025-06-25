import random
from mcrunner import (
    Bar, StrategyBacktester,
    SOrderParameters, Contracts, EOrderAction,
    load_bars_from_file
)

class PriceBreakouts:
    def __init__(self):
        self.EMALength = 50
        self.LookbackPeriod = 10
        self.OrderCreator = None
        self.Bars = None
        self.StrategyInfo = None
        self.ema_values = []
        self.highest = []
        self.lowest = []

    def create(self):
        self.enter_long = self.OrderCreator.market_next_bar(
            SOrderParameters(Contracts.Default(), EOrderAction.Buy))
        self.enter_short = self.OrderCreator.market_next_bar(
            SOrderParameters(Contracts.Default(), EOrderAction.SellShort))
        self.exit_long = self.OrderCreator.market_next_bar(
            SOrderParameters(Contracts.Default(), EOrderAction.Sell))
        self.exit_short = self.OrderCreator.market_next_bar(
            SOrderParameters(Contracts.Default(), EOrderAction.BuyToCover))

    def start_calc(self):
        pass

    def calc_bar(self):
        close = self.Bars.CloseValue
        closes = [b.Close for b in self.Bars.bars]
        if not self.ema_values:
            self.ema_values.append(close)
        else:
            k = 2/(self.EMALength+1)
            self.ema_values.append(k*close + (1-k)*self.ema_values[-1])
        prev = closes[:-1]
        lookback = prev[-self.LookbackPeriod:] if prev else []
        self.highest.append(max(lookback) if lookback else close)
        self.lowest.append(min(lookback) if lookback else close)
        ema = self.ema_values[-1]

        if self.StrategyInfo.MarketPosition == 0 and len(closes) > 1:
            prev_high = self.highest[-2]
            prev_low = self.lowest[-2]
            if close > self.highest[-1] and closes[-2] < prev_high:
                self.enter_long.send()
            elif close < self.lowest[-1] and closes[-2] > prev_low:
                self.enter_short.send()
        elif self.StrategyInfo.MarketPosition > 0 and len(closes) > 1:
            prev_ema = self.ema_values[-2]
            if close < ema and closes[-2] >= prev_ema:
                self.exit_long.send()
        elif self.StrategyInfo.MarketPosition < 0 and len(closes) > 1:
            prev_ema = self.ema_values[-2]
            if close > ema and closes[-2] <= prev_ema:
                self.exit_short.send()


def example(path: str = "MCRunner/Instruments/data/2330 1 Day.txt"):
    try:
        bars = load_bars_from_file(path)
    except FileNotFoundError:
        random.seed(0)
        bars = []
        price = 100.0
        for _ in range(200):
            price += random.gauss(0, 1)
            bars.append(Bar(Open=price, High=price+1, Low=price-1, Close=price, Volume=0))

    tester = StrategyBacktester(PriceBreakouts, bars)
    tester.backtest()
    print("Final Market Position", tester.strategy_info.MarketPosition)
    orders = tester.manager.ExecutedOrders
    position = None
    entry = None
    for o in orders:
        print(f"bar {o.bar_index}: {o.action.name} at {o.price:.2f}")
        if o.action == EOrderAction.Buy:
            position = 'long'
            entry = o
        elif o.action == EOrderAction.SellShort:
            position = 'short'
            entry = o
        elif o.action == EOrderAction.Sell and position == 'long':
            pnl = o.price - entry.price
            print(f" exit long pnl={pnl:.2f}")
            position = None
        elif o.action == EOrderAction.BuyToCover and position == 'short':
            pnl = entry.price - o.price
            print(f" exit short pnl={pnl:.2f}")
            position = None

if __name__ == "__main__":
    example()
