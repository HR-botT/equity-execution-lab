# Broker Implementations and Metrics

## How brokers differ

Even when two brokers offer a “TWAP” algorithm, the implementation can differ across:

1. **Slice granularity and timing** — number of slices, randomisation of intervals, minimum/maximum child size.
2. **Venue preference** — lit-only, dark-first, or conditional dark participation; willingness to use midpoint pegs versus limit orders.
3. **Aggression** — market orders versus passive limits; urgency parameter in the cost model.
4. **Auction handling** — whether the algorithm pauses, accelerates, or participates in the opening/closing cross.
5. **Fee awareness** — whether the router minimises spread cost only or spread + fees + adverse selection.

In this scaffold, broker behaviour is represented by the `SmartOrderRouter` urgency parameter and by the algorithm constructor arguments (slice count, display quantity, `pause_during_auction`). A `broker_profile` dataclass can later bundle these parameters and drive two runs of the same algorithm class.

## Metrics

| Metric | Formula | Interpretation |
|---|---|---|
| **Implementation Shortfall (per share)** | `(avg_price − arrival_price) × sign` | Positive for BUY = cost; negative = saving. The primary decision-cost measure. |
| **VWAP slippage (bps)** | `(avg_price − benchmark_VWAP) / benchmark_VWAP × 10,000` | Execution performance relative to a volume benchmark. |
| **Fill rate** | `filled / target` | Whether the algorithm completed the parent order. |

The `analysis/metrics.py` module implements the first three. Completion time is available from the algorithm’s fill timestamps and can be added to `ExecutionResult` in a later iteration.