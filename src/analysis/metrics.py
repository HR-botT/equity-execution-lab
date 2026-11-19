def implementation_shortfall(side: str, arrival_price: float, fills: list[dict]) -> float:
    """Per-share IS in dollars; positive = cost, negative = saving."""
    if not fills: return 0.0
    total_qty = sum(f["quantity"] for f in fills)
    avg_price = sum(f["price"] * f["quantity"] for f in fills) / total_qty
    return (avg_price - arrival_price) if side == "BUY" else (arrival_price - avg_price)

def vwap_slippage_bps(side: str, avg_price: float, benchmark_vwap: float) -> float:
    if benchmark_vwap == 0: return 0.0
    diff = avg_price - benchmark_vwap if side == "BUY" else benchmark_vwap - avg_price
    return (diff / benchmark_vwap) * 10_000

def fill_rate(filled: int, target: int) -> float:
    return filled / target if target else 0.0