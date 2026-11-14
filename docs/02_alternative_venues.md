# Alternative Venues and Smart Order Routing

## Dark pools

**Why.** Institutional investors use dark pools to execute large orders without displaying intent, reducing market impact and information leakage.

**How.** A dark pool matches orders internally at a reference price (midpoint, VWAP, or NBBO-derived). No pre-trade quote is disseminated. The `core/dark_pool.py` module enforces a minimum block size and matches against the NBBO midpoint.

**Issues.** Dark pools face adverse selection (informed traders may prefer them), fragmentation, and the risk of executing at stale reference prices. Minimum block sizes mitigate but do not eliminate these problems.

## Smart Order Routing

**Why.** Liquidity is fragmented across lit exchanges and dark venues. A router that statically sends everything to one venue will systematically overpay in spread or miss better prices elsewhere.

**How.** The `routing/sor.py` router consumes `VenueSnapshot` objects and scores each venue using a Cont–Kukanov-style static cost model (`routing/cost_model.py`): expected price + fee + an adverse-selection penalty that increases when the venue’s displayed depth is small relative to the child order size. The router allocates to the lowest-cost venue for a single-venue allocation in the current scaffold; multi-venue splitting is a natural extension.