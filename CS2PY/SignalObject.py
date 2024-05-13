from abc import ABC, abstractmethod

class SignalObject(ABC):
    def __init__(self, _):
        self.PositionSide = None
        self.Positions = None
        self.CurrentPosition = None
        self.Portfolio = None
        self.NetProfit = None
        self.AvgBarsEvenTrade = None
        self.AvgBarsLosTrade = None
        self.AvgBarsWinTrade = None
        self.GrossLoss = None
        self.GrossProfit = None
        self.LargestLosTrade = None
        self.LargestWinTrade = None
        self.MaxConsecLosers = None
        self.MaxConsecWinners = None
        self.MaxLotsHeld = None
        self.MaxDrawDown = None
        self.NumEvenTrades = None
        self.NumLosTrades = None
        self.NumWinTrades = None
        self.PercentProfit = None
        self.TotalBarsEvenTrades = None
        self.TotalBarsLosTrades = None
        self.TotalBarsWinTrades = None
        self.TotalTrades = None
        self.Commission = None
        self.Slippage = None
        self.InitialCapital = None
        self.InterestRate = None
        self.StrategyCurrencyCode = None
        self.Account = None
        self.Profile = None
        self.OrderCreator = None
        self.CurSpecOrdersMode = None

    @abstractmethod
    def GenerateStopLoss(self, amount):
        pass

    @abstractmethod
    def GenerateExitOnClose(self):
        pass

    @abstractmethod
    def GenerateDollarTrailing(self, profit):
        pass

    @abstractmethod
    def GenerateATMarketOrder(self, buy, entry, lots):
        pass

    @abstractmethod
    def GenerateProfitTargetPt(self, amount):
        pass

    @abstractmethod
    def GenerateTrailingStopPt(self, amount):
        pass
