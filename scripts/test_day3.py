from datetime import time
from src.core.exchange import Exchange
from src.core.dark_pool import DarkPool
from src.core.order import Order, Side

print("=== Testing Exchange Rules (Nasdaq) ===")
# Load the YAML file we made on Day 1
nasdaq = Exchange("configs/exchanges/nasdaq.yaml")

print(f"Loaded Exchange: {nasdaq.exchange_id}")
print(f"Raw Config Sessions: {nasdaq._sessions}")

# Test if the market is open at different times
time_10am = time(10, 0)
time_5pm = time(17, 0)
time_2am = time(2, 0)

print(f"\nIs 10:00 AM continuous trading? {nasdaq.is_continuous_trading(time_10am)}")
print(f"Is 5:00 PM continuous trading? {nasdaq.is_continuous_trading(time_5pm)}")
print(f"Is 2:00 AM continuous trading? {nasdaq.is_continuous_trading(time_2am)}")

print("\n=== Testing Dark Pool ===")
dp = DarkPool("DARK_A", min_block_size=100)
# Someone wants to sell 300 shares
dp.submit(Order(side=Side.SELL, quantity=300), nbbo_mid=150.00)

# Someone wants to buy 150 shares. Since it's above the 100 min block size, it should fill!
fills = dp.submit(Order(side=Side.BUY, quantity=150), nbbo_mid=150.00)
print(f"Dark pool fills: {fills}")