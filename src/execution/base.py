from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from ..core.order import Side

class AlgoState(Enum):
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    INCOMPLETE = "INCOMPLETE"

@dataclass
class ExecutionResult:
    total_quantity: int
    filled_quantity: int
    avg_price: float | None
    slices_sent: int
    state: AlgoState
    fills: list[dict] = field(default_factory=list)

class ExecutionAlgo(ABC):
    def __init__(self, side: Side, total_quantity: int, arrival_price: float):
        self.side = side
        self.total_quantity = total_quantity
        self.arrival_price = arrival_price
        self.filled = 0
        self.slices_sent = 0
        self.fills: list[dict] = []
        self.state = AlgoState.RUNNING

    @abstractmethod
    def next_slice(self) -> int:
        """Returns the quantity to buy/sell in the next slice."""
        pass

    def record_fill(self, fills: list[dict]):
        for f in fills:
            self.filled += f["quantity"]
            self.fills.append(f)
            
        # Check for completion or edge-case failure
        if self.filled >= self.total_quantity:
            self.state = AlgoState.COMPLETED
        elif self.slices_sent >= self._max_slices() and self.filled < self.total_quantity:
            self.state = AlgoState.INCOMPLETE

    def _max_slices(self) -> int:
        return 1

    def result(self) -> ExecutionResult:
        avg = None
        if self.filled > 0:
            notional = sum(f["price"] * f["quantity"] for f in self.fills)
            avg = notional / self.filled
        return ExecutionResult(self.total_quantity, self.filled, avg, self.slices_sent, self.state, self.fills)