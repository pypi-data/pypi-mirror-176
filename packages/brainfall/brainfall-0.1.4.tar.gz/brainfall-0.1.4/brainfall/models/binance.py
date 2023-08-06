from attrs import define, field
from pandas import Timestamp


@define
class RateLimits:
    rateLimitType: str = field()
    interval: str = field()
    intervalNum: int = field(converter=int)
    limit: int = field(converter=int)


@define
class Symbol:
    symbol: str
    baseAsset: str
    quoteAsset: str
    status: str
    baseAssetPrecision: int = field(converter=int)
    quotePrecision: int = field(converter=int)
    quoteAssetPrecision: int = field(converter=int)
    baseCommissionPrecision: int = field(converter=int)
    quoteCommissionPrecision: int = field(converter=int)
    isSpotTradingAllowed: bool
    isMarginTradingAllowed: bool
    cancelReplaceAllowed: bool
    allowTrailingStop: bool
    quoteOrderQtyMarketAllowed: bool
    icebergAllowed: bool
    ocoAllowed: bool
    orderTypes: list[str]
    permissions: list[str]
    filters: list


class MarketInfo:
    def __init__(
        self, server_time, filters, rate_limits, symbols, tz="UTC", time_unit="ms"
    ):
        self.timezone = tz
        self.filters = filters
        self.rate_limits = [RateLimits(**limit) for limit in rate_limits]
        self.symbols = {values["symbol"]: Symbol(**values) for values in symbols}
        self.server_time = Timestamp(server_time, tz=tz, unit=time_unit)

    @property
    def num_symbols(self):
        """get number of symbols in market"""
        return len(self.symbols)
