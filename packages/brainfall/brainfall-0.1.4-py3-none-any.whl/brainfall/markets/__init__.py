from collections.abc import Callable

from binance.spot import Spot
from binance.websocket.spot.websocket_client import (
    SpotWebsocketClient as WebsocketClient,
)
from pandas import Timestamp

from brainfall.models import CandleData
from brainfall.models.binance import MarketInfo


class Binance:
    """API for Binance Spot and Websocket clients

    This class facilitates requesting historical klines and
    starting or stopping websocket data for symbol/interval
    """

    SUPPORTED_INTERVALS = [
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "4h",
        "6h",
        "8h",
        "12h",
        "1d",
        "3d",
        "1w",
        "1M",
    ]
    KLINES_COLS = {
        "open_time": "datetime64[ms]",
        "open_price": float,
        "high_price": float,
        "low_price": float,
        "close_price": float,
        "volume": float,
        "close_time": "datetime64[ms]",
        "quote_asset_volume": float,
        "num_trades": int,
        "taker_buy_base_asset_volume": float,
        "taker_buy_quote_asset_volume": float,
        "ignore": object,
    }
    KLINE_SOCK_COLS = {  # uses dtypes from KLINES_COLS
        "t": "open_time",
        "o": "open_price",
        "h": "high_price",
        "l": "low_price",
        "c": "close_price",
        "v": "volume",
        "T": "close_time",
        "q": "quote_asset_volume",
        "n": "num_trades",
        "V": "taker_buy_base_asset_volume",
        "Q": "taker_buy_quote_asset_volume",
        "B": "ignore",
    }

    def __init__(self, **kwargs):
        """ign

        Args:
            **kwargs: keyword arguments passed to [Binance.Spot](https://binance-connector.readthedocs.io)
        """
        self.client = Spot(**kwargs)
        self.ws_client = WebsocketClient()
        self.ws_client.start()
        self._active_ws = 0

    def server_time(self) -> Timestamp:
        """Get server time from Binance

        Returns:
            Market server time
        """
        return Timestamp(self.client.time().get("serverTime"), tz="utc", unit="ms")

    def klines(self, symbol: str, interval: str, **kwargs) -> CandleData:
        """Get last 500 klines for the requested symbol/interval

        Args:
            symbol: symbol/pair/ticker name
            interval: klines interval, eg. 1m, 15m, 4h, 1d
            **kwargs: [Binance API docs](https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data)

        Returns:
            The requested klines
        """
        klines = self.client.klines(symbol=symbol, interval=interval, **kwargs)
        return CandleData(data=klines, columns=self.KLINES_COLS)

    def start_kline_socket(
        self, symbol: str, interval: str, callback: Callable
    ) -> None:
        """Start a kline websocket that calls the callback function on every reply

        Args:
            symbol: symbol/pair/ticker name
            interval: klines interval, eg. 1m, 15m, 4h, 1d
            callback: A callable to receive websocket data
        """
        wrapped_callback = self._kline_socket_callback_wrapper(callback)
        self.ws_client.kline(
            callback=wrapped_callback,
            symbol=symbol,
            interval=interval,
            id=self._active_ws + 1,
        )
        self._active_ws += 1

    def stop_kline_socket(self, symbol: str, interval: str) -> None:
        """Stop a kline websocket that was started with Binance.start_kline_socket

        Args:
            symbol: symbol/pair/ticker name
            interval: klines interval, eg. 1m, 15m, 4h, 1d
        """
        self.ws_client.stop_socket(f"{symbol.lower()}@kline_{interval}")

    def market_info(self) -> MarketInfo:
        """Get market info

        Returns:
            Market information, includes: timezone, symbols, filters, and rate limits
        """
        info = self.client.exchange_info()
        return MarketInfo(
            server_time=info["serverTime"],
            filters=info["exchangeFilters"],
            rate_limits=info["rateLimits"],
            symbols=info["symbols"],
            tz=info["timezone"],
            time_unit="ms",
        )

    def stop(self) -> None:
        """Stop websocket client"""
        self.ws_client.stop()

    @staticmethod
    def _kline_socket_callback_wrapper(func: Callable) -> Callable:
        """Websocket callback wrapper for parsing received data

        Args:
            func: A callable that receives

        Returns:
            Wrapped function that parses klines websocket data and forwards it to `func`
        """

        def _socket_callback_wrapper(msg):
            if "result" in msg:
                return
            msg.update(msg.pop("k", {}))
            msg = {
                Binance.KLINE_SOCK_COLS[k]: v
                for k, v in msg.items()
                if k in Binance.KLINE_SOCK_COLS
            }
            data = CandleData(data=[msg], columns=Binance.KLINES_COLS)
            return func(data)

        return _socket_callback_wrapper
