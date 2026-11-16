def uncross(book, auction_orders: list, side: str) -> tuple[float | None, list[dict]]:
    prices = sorted({o.price for o in auction_orders if o.price})
    if not prices: return None, []
    best_price, best_volume = None, -1
    for p in prices:
        demand = sum(o.quantity for o in auction_orders if o.side.value == "BUY" and o.price >= p)
        supply = sum(o.quantity for o in auction_orders if o.side.value == "SELL" and o.price <= p)
        volume = min(demand, supply)
        if volume > best_volume:
            best_price, best_volume = p, volume
    fills = []
    if best_volume > 0:
        fills.append({"price": best_price, "quantity": best_volume, "venue": "AUCTION"})
    return best_price, fills