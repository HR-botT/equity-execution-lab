from .venue_snapshot import VenueSnapshot

def expected_cost(snapshot: VenueSnapshot, side: str, quantity: int, urgency: float = 0.5) -> float:
    """Static Cont-Kukanov-style cost: spread + fee + fill-probability penalty."""
    if side == "BUY":
        if snapshot.best_ask is None: return float("inf")
        price = snapshot.best_ask
        spread = (snapshot.best_ask - snapshot.best_bid) if snapshot.best_bid else 0.01
    else:
        if snapshot.best_bid is None: return float("inf")
        price = snapshot.best_bid
        spread = (snapshot.best_ask - snapshot.best_bid) if snapshot.best_ask else 0.01

    depth = snapshot.ask_size if side == "BUY" else snapshot.bid_size
    fill_probability = min(1.0, depth / max(quantity, 1))
    
    # The higher the urgency, the more we penalize venues with low depth
    adverse_selection = spread * (1.0 - fill_probability) * urgency
    fee = snapshot.fee_per_share if not snapshot.is_dark else 0.0
    
    return price + fee + adverse_selection