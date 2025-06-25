from dataclasses import dataclass, field
from enum import Enum, auto

class EOrderAction(Enum):
    Buy = auto()
    Sell = auto()
    SellShort = auto()
    BuyToCover = auto()

class OrderCategory(Enum):
    Market = auto()
    Limit = auto()
    Stop = auto()
    StopLimit = auto()

class EExitType(Enum):
    All = auto()

@dataclass
class Contracts:
    contract: int = 100
    is_user_specified: bool = False

    @staticmethod
    def Default():
        return Contracts()

    @staticmethod
    def CreateUserSpecified(size: int):
        return Contracts(contract=size, is_user_specified=True)

@dataclass
class OrderExit:
    ExitType: EExitType = EExitType.All

@dataclass
class SOrderParameters:
    contracts: Contracts = field(default_factory=Contracts.Default)
    action: EOrderAction = EOrderAction.Buy
    exit_type_info: OrderExit = field(default_factory=OrderExit)
    name: str = ""
    lots: Contracts = field(default_factory=Contracts.Default)
