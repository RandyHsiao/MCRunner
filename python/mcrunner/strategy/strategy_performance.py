class StrategyPerformance:
    def __init__(self):
        self.MarketPosition = 0
        self.market_position_at_broker = 0

    @property
    def MarketPositionAtBroker(self):
        return int(self.market_position_at_broker)

    def update_market_position_at_broker(self, change: float):
        self.market_position_at_broker += change

    # SetPlotValue/GetPlotValue not implemented
