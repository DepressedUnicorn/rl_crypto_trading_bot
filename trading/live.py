from __future__ import annotations

import random
import time
from datetime import datetime

from analytics.portfolio_tracker import PortfolioTracker


def run_live_trading(tracker: PortfolioTracker, iterations: int = 10) -> None:
    """Simple live-trading loop with portfolio tracking."""
    balance = 1000.0
    pnl = 0.0
    for _ in range(iterations):
        change = random.uniform(-5, 5)
        balance += change
        pnl += change
        tracker.log_snapshot(balance, pnl)
        tracker.log_trade("BTC/USD", 0.1, balance, "buy" if change >= 0 else "sell")
        time.sleep(0.01)
