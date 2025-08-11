"""Binance client wrapper for REST and WebSocket interactions."""
from typing import Callable, Dict, Any, Optional

try:
    from binance.client import Client
    from binance.streams import ThreadedWebsocketManager
except Exception as exc:  # pragma: no cover - external dependency
    raise ImportError("python-binance is required to use BinanceClient") from exc


class BinanceClient:
    """Simple wrapper around :mod:`python-binance` client.

    Parameters
    ----------
    api_key: str, optional
        API key for authenticated endpoints.
    api_secret: str, optional
        API secret for authenticated endpoints.
    testnet: bool, default False
        Whether to use Binance testnet endpoints.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        testnet: bool = False,
    ) -> None:
        self.client = Client(api_key, api_secret, testnet=testnet)
        self._ws_manager: Optional[ThreadedWebsocketManager] = None

    # ------------------------------------------------------------------
    # REST methods
    # ------------------------------------------------------------------
    def get_price_rules(self, symbol: str) -> Dict[str, Any]:
        """Return trading rules for a symbol.

        Parameters
        ----------
        symbol: str
            Market symbol, e.g. ``"BTCUSDT"``.

        Returns
        -------
        dict
            Dictionary with tick size, minimum quantity and related fields.
        """
        info = self.client.get_symbol_info(symbol)
        if info is None:
            raise ValueError(f"Symbol {symbol!r} not found")

        filters = {f["filterType"]: f for f in info.get("filters", [])}
        price_filter = filters.get("PRICE_FILTER", {})
        lot_size = filters.get("LOT_SIZE", {})
        min_notional = filters.get("MIN_NOTIONAL", {})

        return {
            "tick_size": float(price_filter.get("tickSize", 0)),
            "min_price": float(price_filter.get("minPrice", 0)),
            "max_price": float(price_filter.get("maxPrice", 0)),
            "min_qty": float(lot_size.get("minQty", 0)),
            "max_qty": float(lot_size.get("maxQty", 0)),
            "step_size": float(lot_size.get("stepSize", 0)),
            "min_notional": float(min_notional.get("minNotional", 0)),
        }

    # ------------------------------------------------------------------
    # WebSocket methods
    # ------------------------------------------------------------------
    def stream_live_prices(self, symbol: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Stream live ticker prices for ``symbol``.

        Parameters
        ----------
        symbol: str
            Market symbol, e.g. ``"BTCUSDT"``.
        callback: Callable[[Dict[str, Any]], None]
            Function invoked with raw message dictionaries from Binance.
        """
        if self._ws_manager is None:
            self._ws_manager = ThreadedWebsocketManager(client=self.client)
            self._ws_manager.start()

        def _handle(msg: Dict[str, Any]) -> None:
            callback(msg)

        self._ws_manager.start_symbol_ticker_socket(symbol=symbol.lower(), callback=_handle)

    def stop_stream(self) -> None:
        """Stop any open WebSocket streams."""
        if self._ws_manager is not None:
            self._ws_manager.stop()
            self._ws_manager = None
