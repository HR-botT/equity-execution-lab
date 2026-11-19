from .metrics import implementation_shortfall

def compare_brokers(results: dict[str, list[dict]], arrival_price: float, side: str) -> dict:
    comparison = {}
    for broker, fills in results.items():
        if not fills:
            comparison[broker] = {"avg_price": None, "IS_bps": None, "fill_rate": 0.0}
            continue
        total_qty = sum(f["quantity"] for f in fills)
        avg_price = sum(f["price"] * f["quantity"] for f in fills) / total_qty
        is_cost = implementation_shortfall(side, arrival_price, fills)
        is_bps = (is_cost / arrival_price) * 10_000
        comparison[broker] = {
            "avg_price": round(avg_price, 4),
            "IS_bps": round(is_bps, 2),
            "fill_rate": 1.0 if total_qty > 0 else 0.0
        }
    return comparison