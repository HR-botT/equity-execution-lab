from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
import time

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    IOC = "IOC"
    FOK = "FOK"

@dataclass
class Order:
    side: Side
    quantity: int
    order_type: OrderType = OrderType.LIMIT
    price: float | None = None
    order_id: str = field(default_factory=lambda: uuid4().hex[:12])
    timestamp: float = field(default_factory=time.perf_counter)
    displayed_quantity: int | None = None