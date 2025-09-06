import random
from typing import List, Tuple
from mcrunner.instruments import load_bars_from_file


def exponential_moving_average(data: List[float], length: int) -> List[float]:
    ema = []
    alpha = 2 / (length + 1)
    for i, value in enumerate(data):
        if i == 0:
            ema.append(value)
        else:
            ema.append(alpha * value + (1 - alpha) * ema[i - 1])
    return ema


def rolling_max(data: List[float], window: int) -> List[float]:
    result = []
    for i in range(len(data)):
        if i == 0:
            result.append(data[0])
        elif i < window:
            result.append(max(data[:i]))
        else:
            result.append(max(data[i - window:i]))
    return result


def rolling_min(data: List[float], window: int) -> List[float]:
    result = []
    for i in range(len(data)):
        if i == 0:
            result.append(data[0])
        elif i < window:
            result.append(min(data[:i]))
        else:
            result.append(min(data[i - window:i]))
    return result


def price_breakouts(close: List[float], ema_length: int = 50, lookback_period: int = 10) -> List[Tuple[str, int, float]]:
    ema = exponential_moving_average(close, ema_length)
    highest = rolling_max(close[:-1], lookback_period) + [max(close[-lookback_period:])]
    lowest = rolling_min(close[:-1], lookback_period) + [min(close[-lookback_period:])]

    position = 0
    trades = []
    for i in range(1, len(close)):
        c = close[i]
        c_prev = close[i - 1]
        hi = highest[i]
        hi_prev = highest[i - 1]
        lo = lowest[i]
        lo_prev = lowest[i - 1]
        e = ema[i]
        e_prev = ema[i - 1]

        if position == 0:
            if c > hi and c_prev < hi_prev:
                position = 1
                trades.append(('buy', i, c))
            elif c < lo and c_prev > lo_prev:
                position = -1
                trades.append(('sell_short', i, c))
        elif position == 1:
            if c < e and c_prev >= e_prev:
                position = 0
                trades.append(('exit_long', i, c))
        elif position == -1:
            if c > e and c_prev <= e_prev:
                position = 0
                trades.append(('exit_short', i, c))
    return trades


def example_run(path: str = "MCRunner/Instruments/data/2330 1 Day.txt"):
    try:
        bars = load_bars_from_file(path)
        close_prices = [b.Close for b in bars]
    except FileNotFoundError:
        random.seed(0)
        close_prices = []
        price = 100.0
        for _ in range(200):
            price += random.gauss(0, 1)
            close_prices.append(price)

    trades = price_breakouts(close_prices)
    for t in trades:
        print(t)


if __name__ == "__main__":
    example_run()
