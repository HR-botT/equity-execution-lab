# US Equity Market Microstructure

## NASDAQ

**Sessions (ET).** Pre-market 07:00–09:30; regular 09:30–16:00; after-hours 16:00–20:00. Quotes and orders are accepted from 07:00 to 20:00.

**Opening and closing crosses.** NASDAQ disseminates Net Order Imbalance Indicator (NOII) information from 09:25 for the Opening Cross and from 15:50 for the Closing Cross. Limit orders entered after 09:28 for the Opening Cross are treated as Imbalance-Only (IO) and execute only during the cross.

**Order types.** Market, Limit, IOC, FOK, MOO, LOO, MOC, LOC, IO, midpoint peg, primary peg, Reserve (iceberg), and Non-Display are supported.

**Matching priority.** NASDAQ uses **Price/Time** priority: displayed interest ranks before non-displayed interest at the same price, and time is the secondary priority within each category. Odd-lot orders rank below round lots at the same price.

## NYSE

**Opening auction.** Pillar Gateways open for order entry at 06:30; imbalance information is disseminated from 08:00; the opening process begins at 09:30. The DMM may open securities algorithmically within ±10% of the reference price; outside that range, a manual opening is required.

**Closing auction.** MOC and LOC orders can be entered, modified, or cancelled until **15:50**. After 15:50, they can only be entered on the contra side of a significant imbalance until 16:00, and cannot be modified or cancelled. The closing cross occurs at 16:00.

**Matching priority.** NYSE uses a **Parity/Priority** model, not pure price-time. The participant setting the interest receives 15% of the executed volume (or one round lot, whichever is greater); the remainder is allocated on **parity** among participants at the same price, rather than by time priority. This design is intended to reward posted liquidity rather than speed.

## Fee structure (illustrative)

- NASDAQ: maker rebate ≈ $0.0020/share, taker fee ≈ $0.0030/share (tiered by volume and symbol).
- NYSE: adding displayed liquidity rebate ≈ $0.0020/share (Tier 2 Tape A example); removing liquidity fee ≈ $0.0030/share.

## Matching-rule summary

| Venue | Priority | Displayed vs non-displayed | Auction model |
|---|---|---|---|
| NASDAQ | Price/Time | Displayed first | NOII-driven cross |
| NYSE | Parity/Priority (15% setter) | Displayed first, parity for remainder | DMM-facilitated call auction |