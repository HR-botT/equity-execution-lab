from src.routing.venue_snapshot import VenueSnapshot
from src.routing.sor import SmartOrderRouter
from src.analysis.metrics import implementation_shortfall, vwap_slippage_bps

print("=== Testing Smart Order Router ===")
# NASDAQ is cheaper, but has very little volume (100 shares)
nasdaq = VenueSnapshot(venue_id="NASDAQ", best_ask=150.00, ask_size=100, best_bid=149.99, bid_size=100, fee_per_share=0.003)
# NYSE is slightly more expensive, but has lots of volume (5000 shares)
nyse = VenueSnapshot(venue_id="NYSE", best_ask=150.01, ask_size=5000, best_bid=150.00, bid_size=5000, fee_per_share=0.002)

router = SmartOrderRouter(urgency=0.8)

# Scenario A: We only want to buy 50 shares. NASDAQ should win (cheaper + enough volume)
venue_a, qty_a, cost_a = router.route("BUY", 50, [nasdaq, nyse])
print(f"Order 50 shares -> Routed to {venue_a} (Cost: ${cost_a:.4f})")

# Scenario B: We want to buy 1,000 shares. NASDAQ doesn't have enough volume!
# The router should penalize NASDAQ for low fill probability and route to NYSE.
venue_b, qty_b, cost_b = router.route("BUY", 1000, [nasdaq, nyse])
print(f"Order 1000 shares -> Routed to {venue_b} (Cost: ${cost_b:.4f})")

print("\n=== Testing TCA Metrics ===")
# Let's pretend our TWAP bot bought 1,000 shares at an average price of $150.05
# even though the arrival price was $150.00
fills = [{"price": 150.05, "quantity": 1000}]
is_cost = implementation_shortfall("BUY", arrival_price=150.00, fills=fills)
print(f"Implementation Shortfall: ${is_cost:.4f} per share (We paid 5 cents above arrival)")

# VWAP Slippage
slippage = vwap_slippage_bps("BUY", avg_price=150.05, benchmark_vwap=150.00)
print(f"VWAP Slippage: {slippage:.2f} bps (Basis points)")