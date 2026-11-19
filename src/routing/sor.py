from .venue_snapshot import VenueSnapshot
from .cost_model import expected_cost

class SmartOrderRouter:
    def __init__(self, urgency: float = 0.5):
        self.urgency = urgency

    def route(self, side: str, quantity: int, snapshots: list[VenueSnapshot]) -> tuple[str, int, float]:
        """Returns (venue_id, quantity, expected_cost) for the best venue."""
        scored = []
        for s in snapshots:
            c = expected_cost(s, side, quantity, self.urgency)
            scored.append((c, s))
            
        scored.sort(key=lambda x: x[0])
        best_cost, best = scored[0]
        
        return best.venue_id, quantity, best_cost