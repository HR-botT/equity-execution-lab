from .base import ExecutionAlgo, AlgoState
from ..core.order import Side

class Decipher(ExecutionAlgo):
    """Adaptive execution based on a momentum signal."""
    def __init__(self, side: Side, total_quantity: int, arrival_price: float, base_slices: int, signal_strength: float):
        super().__init__(side, total_quantity, arrival_price)
        self.base_slices = base_slices
        self.signal_strength = max(0.0, min(1.0, signal_strength))
        self._slice_qty = total_quantity // base_slices
        self._remainder = total_quantity % base_slices

    def _max_slices(self) -> int:
        return self.base_slices

    def next_slice(self) -> int:
        if self.state != AlgoState.RUNNING: return 0
        if self.slices_sent >= self.base_slices:
            if self.filled < self.total_quantity: 
                self.state = AlgoState.INCOMPLETE
            return 0
            
        # If signal is strong (1.0), we buy 50% more; if weak (0.0), 50% less.
        multiplier = 0.5 + self.signal_strength
        base_qty = self._slice_qty + (1 if self.slices_sent < self._remainder else 0)
        
        qty = int(round(base_qty * multiplier))
        qty = min(qty, self.total_quantity - self.filled)
        
        self.slices_sent += 1
        return qty