from dataclasses import dataclass

@dataclass(frozen=True)
class VenueSnapshot:
    venue_id: str
    best_ask: float | None
    ask_size: int
    best_bid: float | None
    bid_size: int
    fee_per_share: float = 0.0
    rebate_per_share: float = 0.0
    is_dark: bool = False