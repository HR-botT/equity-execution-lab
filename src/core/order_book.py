from collections import defaultdict
from .order import Order, Side, OrderType

class OrderBook:
    """Price-time priority book for a single lit venue."""
    
    def __init__(self):
        self.bids: dict[float, list[Order]] = defaultdict(list)
        self.asks: dict[float, list[Order]] = defaultdict(list)
        self.fills: list[dict] = []

    def add(self, order: Order):
        book = self.bids if order.side == Side.BUY else self.asks
        book[order.price].append(order)

    def best_bid(self) -> float | None:
        return max(self.bids) if self.bids else None

    def best_ask(self) -> float | None:
        return min(self.asks) if self.asks else None

    def match(self, incoming: Order) -> list[dict]:
        if incoming.order_type == OrderType.MARKET:
            return self._match_market(incoming)
        return self._match_limit(incoming)

    def _match_market(self, incoming: Order) -> list[dict]:
        book = self.asks if incoming.side == Side.BUY else self.bids
        fills, remaining = [], incoming.quantity
        
        # Get prices in order of best to worst
        levels = sorted(book.keys()) if incoming.side == Side.BUY else sorted(book.keys(), reverse=True)
        
        for price in levels:
            if remaining <= 0: break
            queue = book[price]
            while queue and remaining > 0:
                resting = queue[0]
                take = min(remaining, resting.quantity)
                fills.append({"price": price, "quantity": take, "maker": resting.order_id, "taker": incoming.order_id})
                resting.quantity -= take
                remaining -= take
                if resting.quantity == 0: queue.pop(0)
            if not queue: del book[price]
            
        self.fills.extend(fills)
        return fills

    def _match_limit(self, incoming: Order) -> list[dict]:
        opposite = self.asks if incoming.side == Side.BUY else self.bids
        fills, remaining = [], incoming.quantity
        
        while remaining > 0:
            best = min(opposite) if incoming.side == Side.BUY else max(opposite)
            if best is None: break
            
            # Check if the best price on the book crosses the incoming limit price
            if incoming.side == Side.BUY and best > incoming.price: break
            if incoming.side == Side.SELL and best < incoming.price: break
            
            queue = opposite[best]
            while queue and remaining > 0:
                resting = queue[0]
                take = min(remaining, resting.quantity)
                fills.append({"price": best, "quantity": take, "maker": resting.order_id, "taker": incoming.order_id})
                resting.quantity -= take
                remaining -= take
                if resting.quantity == 0: queue.pop(0)
            if not queue: del opposite[best]
            
        self.fills.extend(fills)
        return fills

    def depth_at(self, side: Side, price: float) -> int:
        book = self.bids if side == Side.BUY else self.asks
        return sum(o.quantity for o in book.get(price, []))