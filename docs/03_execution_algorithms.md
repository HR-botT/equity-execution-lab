# Agency Execution Algorithms

## Base contract

Every algorithm subclasses `execution/base.py::ExecutionAlgo` and implements `next_slice()`. The base class owns the completion state (`RUNNING`, `PAUSED`, `COMPLETED`, `INCOMPLETE`) and records fills via `record_fill()`. This is the hook for the **order-incompletion** edge case: an algorithm that has sent all of its planned slices but has not filled the parent quantity transitions to `INCOMPLETE` instead of silently stopping.

## TWAP

Slices the parent order into equal child quantities at equal time intervals. The number of slices is a constructor parameter. `pause_during_auction=True` prevents the algorithm from sending child orders during a call auction (the **auction** edge case).

## VWAP

Follows a normalized cumulative volume curve. At tick `i`, the target cumulative filled quantity is `total_quantity × curve[i]`. The child order quantity is the difference between the target and the already-filled quantity. This structure makes the algorithm naturally responsive to **inadequate liquidity**: if a slice underfills, the next slice’s quantity is correspondingly larger (subject to available depth).

## Iceberg

Displays only `display_quantity` shares at a time, replenishing from a hidden reserve. The `max_refills` parameter bounds the number of replenishments. If `max_refills` is exhausted before the parent quantity is filled, the state becomes `INCOMPLETE`.

## Whisper and Decipher

Whisper is a dark-pool-seeking algorithm: it routes child orders to dark venues before lit venues to avoid information leakage. Decipher (per the eFX strategy guide) conditionally interacts with liquidity based on a signal; in this scaffold, the dark pool preference and conditional participation are represented by the `DarkPool` class and the router’s `is_dark` flag.