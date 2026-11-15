from src.core.order import Order, Side, OrderType
from src.core.matching_engine import MatchingEngine

def run_test():
    print("=== Initializing Matching Engine ===")
    engine = MatchingEngine()

    print("\n=== Step 1: Sellers enter the book ===")
    # Seller A wants to sell 100 shares at $150.00
    engine.book.add(Order(side=Side.SELL, quantity=100, price=150.00))
    # Seller B wants to sell 50 shares at $150.50
    engine.book.add(Order(side=Side.SELL, quantity=50, price=150.50))
    
    print(f"Best Ask (Lowest sell price): ${engine.book.best_ask()}")
    print(f"Best Bid (Highest buy price): {engine.book.best_bid()}")

    print("\n=== Step 2: Buyer arrives (Partial Fill) ===")
    # Buyer wants to buy 120 shares, but only wants to pay up to $150.00
    buy_order = Order(side=Side.BUY, quantity=120, order_type=OrderType.LIMIT, price=150.00)
    fills = engine.submit(buy_order)

    for fill in fills:
        print(f"FILL: Bought {fill['quantity']} shares at ${fill['price']}")

    # Let's check the state of the book
    print(f"\nBest Ask now: ${engine.book.best_ask()} (Seller B is still there)")
    print(f"Remaining shares resting on Bid at $150.00: {engine.book.depth_at(Side.BUY, 150.00)}")
    
    print("\n=== Step 3: Another Buyer arrives (Complete Fill) ===")
    # Buyer 2 wants to buy the remaining 50 shares at $150.50
    buy_order_2 = Order(side=Side.BUY, quantity=50, order_type=OrderType.LIMIT, price=150.50)
    fills_2 = engine.submit(buy_order_2)
    
    for fill in fills_2:
        print(f"FILL: Bought {fill['quantity']} shares at ${fill['price']}")
        
    print(f"\nBest Ask now: {engine.book.best_ask()} (Book is empty)")
    print(f"Best Bid now: ${engine.book.best_bid()} (Buyer 1's 20 shares are still sitting here)")

if __name__ == "__main__":
    run_test()