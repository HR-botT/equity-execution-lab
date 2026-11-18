from .base import ExecutionAlgo, AlgoState
from ..core.order import Side

class Iceberg(ExecutionAlgo):
    def __init__(self, side: Side, total_quantity: int, arrival_price: float, display_quantity: int, max_refills: int = 100):
        super().__init__(side, total_quantity, arrival_price)
        self.display_quantity = display_quantity
        self.max_refills = max_refills
        self.refills = 0

    def _max_slices(self) -> int:
        return self.max_refills

    def next_slice(self) -> int:
        if self.state != AlgoState.RUNNING: return 0
        
        if self.refills >= self.max_refills:
            if self.filled < self.total_quantity: 
                self.state = AlgoState.INCOMPLETE
            return 0
            
        # Only ever show 'display_quantity' to the market
        qty = min(self.display_quantity, self.total_quantity - self.filled)
        if qty <= 0:
            self.state = AlgoState.COMPLETED
            return 0
            
        self.refills += 1
        self.slices_sent += 1
        return qty