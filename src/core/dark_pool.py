from .order import Order, Side

class DarkPool:
    def __init__(self, venue_id: str, min_block_size: int = 200, matching: str = "midpoint"):
        self.venue_id = venue_id
        self.min_block_size = min_block_size
        self.matching = matching
        self.resting: list[Order] = []

    def submit(self, order: Order, nbbo_mid: float | None) -> list[dict]:
        if nbbo_mid is None or order.quantity < self.min_block_size:
            return []
        fills, remaining = [], order.quantity
        for resting in list(self.resting):
            if remaining <= 0: break
            if resting.side == order.side: continue
            take = min(remaining, resting.quantity)
            fills.append({"price": nbbo_mid, "quantity": take, "venue": self.venue_id})
            resting.quantity -= take
            remaining -= take
            if resting.quantity == 0: self.resting.remove(resting)
        if remaining > 0:
            order.quantity = remaining
            self.resting.append(order)
        return fills