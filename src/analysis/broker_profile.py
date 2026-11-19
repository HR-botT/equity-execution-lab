from dataclasses import dataclass

@dataclass
class BrokerProfile:
    name: str
    aggression: float
    dark_pool_bias: float
    slice_variance: float
    auction_participation: bool

    def __post_init__(self):
        if not (0.0 <= self.aggression <= 1.0): raise ValueError("Aggression must be 0.0-1.0")
        if not (0.0 <= self.dark_pool_bias <= 1.0): raise ValueError("Dark pool bias must be 0.0-1.0")