"""Paper trading module to simulate order fills and maintain a virtual portfolio.

This module is intentionally lightweight so that it can be used both in unit tests
and simple reinforcement learning experiments.  It keeps track of a cash balance
and per-symbol holdings.  Prices are supplied externally via ``update_price``
which makes it compatible with live price streams or any other data source.
Orders can be executed through ``execute_order`` where the RL agent decides the
symbol, side and quantity.

Example
-------
>>> trader = PaperTrader(1000)
>>> trader.update_price('BTC', 25000)
>>> trader.execute_order('BTC', 'buy', 0.01)
>>> trader.summary()['positions']['BTC']['quantity']
0.01
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Position:
    """Simple position container."""

    quantity: float = 0.0
    last_price: float = 0.0

    @property
    def market_value(self) -> float:
        """Return the market value of this position."""
        return self.quantity * self.last_price


@dataclass
class PaperTrader:
    """Simulates order fills and maintains a virtual trading account."""

    starting_cash: float = 0.0
    cash: float = field(init=False)
    positions: Dict[str, Position] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.cash = float(self.starting_cash)

    # ------------------------------------------------------------------ prices
    def update_price(self, symbol: str, price: float) -> None:
        """Update the last seen price for ``symbol``.

        Parameters
        ----------
        symbol:
            Asset ticker symbol.
        price:
            Latest traded price.
        """
        position = self.positions.setdefault(symbol, Position())
        position.last_price = float(price)

    # ------------------------------------------------------------------ orders
    def execute_order(self, symbol: str, side: str, quantity: float) -> None:
        """Execute an order at the last seen price.

        Parameters
        ----------
        symbol:
            Asset ticker symbol.
        side:
            Either ``"buy"`` or ``"sell"`` (case insensitive).
        quantity:
            Number of units to transact.  For crypto this can be a fractional
            amount.  The trade is filled at the last price supplied via
            :meth:`update_price`.
        """
        side = side.lower()
        if side not in {"buy", "sell"}:
            raise ValueError("side must be 'buy' or 'sell'")

        if symbol not in self.positions or self.positions[symbol].last_price == 0:
            raise ValueError(f"No price available for symbol '{symbol}'")

        price = self.positions[symbol].last_price
        cost = quantity * price

        if side == "buy":
            if cost > self.cash:
                raise ValueError("Insufficient cash for purchase")
            self.cash -= cost
            self.positions[symbol].quantity += quantity
        else:  # sell
            if quantity > self.positions[symbol].quantity:
                raise ValueError("Insufficient quantity to sell")
            self.cash += cost
            self.positions[symbol].quantity -= quantity

    # ------------------------------------------------------------------ account
    def portfolio_value(self) -> float:
        """Return current total account value (cash + market value)."""
        return self.cash + sum(p.market_value for p in self.positions.values())

    def reset(self) -> None:
        """Reset account to initial state."""
        self.cash = float(self.starting_cash)
        self.positions.clear()

    def summary(self) -> Dict[str, object]:
        """Return a dictionary summarising the account state."""
        return {
            "cash": self.cash,
            "positions": {
                symbol: {
                    "quantity": pos.quantity,
                    "last_price": pos.last_price,
                    "market_value": pos.market_value,
                }
                for symbol, pos in self.positions.items()
            },
            "portfolio_value": self.portfolio_value(),
        }

