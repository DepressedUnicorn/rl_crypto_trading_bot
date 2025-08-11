from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import matplotlib.pyplot as plt


@dataclass
class PortfolioSnapshot:
    """State of the portfolio at a given time."""
    timestamp: datetime
    balance: float
    pnl: float


@dataclass
class TradeRecord:
    """Record of a trade executed by the bot."""
    timestamp: datetime
    pair: str
    quantity: float
    price: float
    side: str


class PortfolioTracker:
    """Tracks balances, PnL, and trades for analysis."""

    def __init__(self) -> None:
        self.history: List[PortfolioSnapshot] = []
        self.trades: List[TradeRecord] = []

    def log_snapshot(
        self, balance: float, pnl: float, timestamp: Optional[datetime] = None
    ) -> None:
        """Append a snapshot of the portfolio."""
        ts = timestamp or datetime.utcnow()
        self.history.append(PortfolioSnapshot(ts, balance, pnl))

    def log_trade(
        self,
        pair: str,
        quantity: float,
        price: float,
        side: str,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """Append a trade to the log."""
        ts = timestamp or datetime.utcnow()
        self.trades.append(TradeRecord(ts, pair, quantity, price, side))

    def plot_portfolio_history(self, output_path: Optional[str] = None) -> None:
        """Plot balance and PnL over time.

        Parameters
        ----------
        output_path:
            File to save the figure to. If ``None`` the plot is displayed instead.
        """
        if not self.history:
            raise ValueError("No portfolio history to plot.")

        times = [snap.timestamp for snap in self.history]
        balances = [snap.balance for snap in self.history]
        pnls = [snap.pnl for snap in self.history]

        fig, ax1 = plt.subplots()
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Balance", color="tab:blue")
        ax1.plot(times, balances, color="tab:blue", label="Balance")
        ax1.tick_params(axis="y", labelcolor="tab:blue")

        ax2 = ax1.twinx()
        ax2.set_ylabel("PnL", color="tab:green")
        ax2.plot(times, pnls, color="tab:green", label="PnL")
        ax2.tick_params(axis="y", labelcolor="tab:green")

        fig.tight_layout()
        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(out)
        else:
            plt.show()
        plt.close(fig)
