from src.core.order import Side
from src.execution.twap import TWAP

if __name__ == "__main__":
    print("=== Testing TWAP Algorithm ===")
    
    # We want to buy 10,000 shares, sliced into 10 chunks (1,000 shares each)
    algo = TWAP(side=Side.BUY, total_quantity=10000, arrival_price=150.00, slices=10)

    # Call next_slice() 5 times to see the first half of the plan
    for i in range(5):
        qty = algo.next_slice()
        print(f"Slice {i+1}: Send child order for {qty} shares")