from .order import Order, Side, OrderType
from .order_book import OrderBook

class MatchingEngine:
    def __init__(self, priority: str = "price_time"):
        self.book = OrderBook()
        self.priority = priority

    def submit(self, order: Order) -> list[dict]:
        # 1. Handle IOC (Immediate or Cancel) - change to Market to get filled immediately
        if order.order_type == OrderType.IOC:
            order.order_type = OrderType.MARKET
            
        fills = self.book.match(order)
        
        # 2. Handle FOK (Fill or Kill) - rollback if not fully filled
        if order.order_type == OrderType.FOK:
            total = sum(f["quantity"] for f in fills)
            if total < order.quantity:
                self.book.fills = [f for f in self.book.fills if f not in fills]
                return []
                
        # 3. Handle Limit orders - if there's leftover quantity, add to the book
        if order.order_type not in (OrderType.IOC, OrderType.FOK) and sum(f["quantity"] for f in fills) < order.quantity:
            remaining = order.quantity - sum(f["quantity"] for f in fills)
            rest = Order(side=order.side, quantity=remaining, order_type=OrderType.LIMIT, price=order.price)
            self.book.add(rest)
            
        return fills