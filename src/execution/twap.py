from .base import ExecutionAlgo, AlgoState
from ..core.order import Side

class TWAP(ExecutionAlgo):
    def __init__(self, side: Side, total_quantity: int, arrival_price: float, slices: int, pause_during_auction: bool = True):
        super().__init__(side, total_quantity, arrival_price)
        self.slices = slices
        self.pause_during_auction = pause_during_auction
        self._slice_qty = total_quantity // slices
        self._remainder = total_quantity % slices
        self._auction_paused = False

    def _max_slices(self) -> int:
        return self.slices

    def next_slice(self) -> int:
        if self.state != AlgoState.RUNNING: return 0
        if self.pause_during_auction and self._auction_paused: return 0
        
        # If we've sent all our planned slices, but haven't filled the order, mark it INCOMPLETE
        if self.slices_sent >= self.slices:
            if self.filled < self.total_quantity: 
                self.state = AlgoState.INCOMPLETE
            return 0
            
        # Distribute the remainder evenly across the first few slices
        qty = self._slice_qty + (1 if self.slices_sent < self._remainder else 0)
        qty = min(qty, self.total_quantity - self.filled) # Don't overfill
        self.slices_sent += 1
        return qty

    def enter_auction(self):
        self._auction_paused = True
        self.state = AlgoState.PAUSED

    def exit_auction(self):
        self._auction_paused = False
        if self.state == AlgoState.PAUSED: 
            self.state = AlgoState.RUNNING