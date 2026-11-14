# Equity Execution Lab

> An event-driven simulation platform for US market microstructure, execution algorithms, and Smart Order Routing (SOR).

## Overview

This repository is a deterministic, offline sandbox for researching algorithmic execution. It models NASDAQ and NYSE session rules from YAML configuration, implements a price-time matching engine and a dark pool, and provides base implementations of TWAP, VWAP, Iceberg, Whisper, and Decipher. A Smart Order Router allocates child orders across venues using a static cost model, and a metrics module computes Implementation Shortfall and VWAP slippage.

## Quick Start

Install dependencies:
```bash
pip install -r requirements-dev.txt
```

Run the test suite:
```bash
make test
```

Run a TWAP simulation scenario:
```bash
python -m src.simulation.scenario_runner --scenario configs/scenarios/normal_liquidity.yaml --algo twap
```

## Repository Structure

- `configs/` — Declarative exchange, venue, and scenario definitions (YAML).
- `src/core/` — Order book, matching engine, exchange session state, dark pool, auction.
- `src/execution/` — TWAP, VWAP, Iceberg, Whisper, and Decipher algorithms on a shared base.
- `src/routing/` — Smart Order Router and cost model.
- `src/analysis/` — Implementation Shortfall, VWAP slippage, fill-rate metrics, broker comparison.
- `src/simulation/` — Event loop and scenario runner.
- `tests/` — Behavioural tests including the three required edge cases.
- `docs/` — Research report answering Task 01–04 of the prompt.

## Research Context

This project was built as part of an internship assignment to understand and implement US equity market microstructure, dark pools, smart order routing, and algorithmic execution strategies. The `docs/` folder contains the full research report addressing the theoretical foundations of these systems.