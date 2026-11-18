from .base import ExecutionAlgo, AlgoState
from ..core.order import Side

class VWAP(ExecutionAlgo):
    def __init__(self, side: Side, total_quantity: int, arrival_price: float, volume_curve: list[float], tick: int = 0):
        super().__init__(side, total_quantity, arrival_price)
        self.volume_curve = volume_curve
        self.tick = tick

    def _max_slices(self) -> int:
        return len(self.volume_curve)

    def next_slice(self) -> int:
        if self.state != AlgoState.RUNNING: return 0
        
        if self.tick >= len(self.volume_curve):
            if self.filled < self.total_quantity: 
                self.state = AlgoState.INCOMPLETE
            return 0
            
        # Target how much we SHOULD have filled by this point in time
        target = int(round(self.total_quantity * self.volume_curve[self.tick]))
        # Buy the difference between the target and what we already have
        qty = max(0, target - self.filled)
        
        self.tick += 1
        self.slices_sent += 1
        return qty