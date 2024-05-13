from Instruments import Bars

bars = Bars()

class PriceBreakouts:
    def __init__(self, ctx):
        self.ctx = ctx
        self.EMALength = 50
        self.LookbackPeriod = 10
        self.enterLong = None
        self.enterShort = None
        self.exitLong = None
        self.exitShort = None
        self.EMA = None
        self.lowestClose = None
        self.highestClose = None
        self.emaValues = None

    def create(self):
        # Assuming OrderCreator and VariableSeries are defined elsewhere
        self.enterLong = OrderCreator.market_next_bar(SOrderParameters(Contracts.Default, EOrderAction.Buy))
        self.enterShort = OrderCreator.market_next_bar(SOrderParameters(Contracts.Default, EOrderAction.SellShort))
        self.exitLong = OrderCreator.market_next_bar(SOrderParameters(Contracts.Default, EOrderAction.Sell))
        self.exitShort = OrderCreator.market_next_bar(SOrderParameters(Contracts.Default, EOrderAction.BuyToCover))

        self.lowestClose = VariableSeries(self)
        self.highestClose = VariableSeries(self)
        self.emaValues = VariableSeries(self)

        self.EMA = XAverage(self)

    def start_calc(self):
        self.EMA.length = self.EMALength
        self.EMA.price = bars.close

    def calc_bar(self):
        self.lowestClose.value = bars.close.lowest(self.LookbackPeriod, 1)
        self.highestClose.value = bars.close.highest(self.LookbackPeriod, 1)
        self.emaValues.value = self.EMA[0]

        if StrategyInfo.MarketPosition == 0:
            if (bars.close[0] > self.highestClose[0]) and (bars.close[1] < self.highestClose[1]):
                self.enterLong.send()
            elif (bars.close[0] < self.lowestClose[0]) and (bars.close[1] > self.lowestClose[1]):
                self.enterShort.send()
        elif StrategyInfo.MarketPosition > 0:
            if (bars.close[0] < self.emaValues[0]) and (bars.close[1] >= self.emaValues[1]):
                self.exitLong.send()
        elif StrategyInfo.MarketPosition < 0:
            if (bars.close[0] > self.emaValues[0]) and (bars.close[1] <= self.emaValues[1]):
                self.exitShort.send()

        StrategyInfo.set_plot_value(1, self.lowestClose[0])
        StrategyInfo.set_plot_value(2, self.highestClose[0])
        StrategyInfo.set_plot_value(3, self.emaValues[0])



# class PriceBreakouts:
#     def __init__(self, ctx):
#         self.ctx = ctx
#         self.EMALength = 50
#         self.LookbackPeriod = 10
#         # 初始化其他屬性

#     def create(self):
#         # 初始化訂單和變數系列

#     def start_calc(self):
#         # 設置EMA的長度和價格

#     def calc_bar(self, bar):
#         # 在每個數據點上調用策略邏輯
#         # 例如：
#         self.lowestClose.value = bar.Close.lowest(self.LookbackPeriod, 1)
#         self.highestClose.value = bar.Close.highest(self.LookbackPeriod, 1)
#         self.emaValues.value = self.EMA[0]

#         # 決策點
#         if StrategyInfo.MarketPosition == 0:
#             if (bar.Close[0] > self.highestClose[0]) and (bar.Close[1] < self.highestClose[1]):
#                 self.enterLong.send()
#             elif (bar.Close[0] < self.lowestClose[0]) and (bar.Close[1] > self.lowestClose[1]):
#                 self.enterShort.send()
#         # 其他決策點

#     def run_backtest(self, historical_data):
#         for bar in historical_data:
#             self.calc_bar(bar)
