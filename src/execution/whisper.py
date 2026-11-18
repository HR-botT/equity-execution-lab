from .base import ExecutionAlgo, AlgoState
from ..core.order import Side

class Whisper(ExecutionAlgo):
    """Prioritizes dark pools to avoid information leakage."""
    def __init__(self, side: Side, total_quantity: int, arrival_price: float, slices: int, dark_venues: list[str]):
        super().__init__(side, total_quantity, arrival_price)
        self.slices = slices
        self.dark_venues = dark_venues
        self._slice_qty = total_quantity // slices
        self._remainder = total_quantity % slices

    def _max_slices(self) -> int:
        return self.slices

    def next_slice(self) -> int:
        if self.state != AlgoState.RUNNING: return 0
        if self.slices_sent >= self.slices:
            if self.filled < self.total_quantity: 
                self.state = AlgoState.INCOMPLETE
            return 0
            
        qty = self._slice_qty + (1 if self.slices_sent < self._remainder else 0)
        qty = min(qty, self.total_quantity - self.filled)
        self.slices_sent += 1
        return qty

    def get_preferred_venues(self) -> list[str]:
        return self.dark_venues