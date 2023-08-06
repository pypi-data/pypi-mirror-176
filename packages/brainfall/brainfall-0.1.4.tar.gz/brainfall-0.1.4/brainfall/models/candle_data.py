from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


class OutdatedUpdateError(Exception):
    pass


class CandleData:
    """Stores candle data and indexes them by the 'open_time' column"""

    def __init__(self, data: Iterable | dict | pd.DataFrame, columns: dict | None):
        """ign

        Args:
            data: candle data passed to [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
            columns: ordered labels for data columns each with a dtype {"col_name": data_type}
                if None then columns labels and index are not set
        """
        self.data = pd.DataFrame(data, columns=list(columns) if columns else None)
        if columns:
            self.data = self.data.astype(columns).set_index("open_time")
        self._time_created = pd.Timestamp.utcnow()
        self._time_updated = pd.Timestamp.utcnow()

    @property
    def open_time(self):
        """get all candles open time"""
        return self.data.index.values

    def update(self, other: CandleData) -> None:
        """update in-place with newer one-row data (e.g. stream data).
        If 'other' open_time is same as most recent open time, overwrite
        the most recent data. Otherwise, a new row with newer open_time
        is created and the oldest row is discarded.

        Examples:
            >>> candles = CandleData([[1, 10]], columns={"open_time": int, "price": int})
            >>> candles.data.to_dict(orient="index")
            {1: {'price': 10}}
            >>> candles.update(CandleData([[1, 15]], columns={"open_time": int, "price": int}))
            >>> candles.data.to_dict(orient="index")
            {1: {'price': 15}}
            >>> candles.update(CandleData([[2, 20]], columns={"open_time": int, "price": int}))
            >>> candles.data.to_dict(orient="index")
            {2: {'price': 20}}

        Args:
            other: a one row CandleData to update last open candle

        Raises:
            OutdatedUpdateError: if 'other' contains outdated data
        """
        if self.open_time[-1] > other.open_time[0]:
            raise OutdatedUpdateError("Can't update with old data")
        if self.open_time[-1] < other.open_time[0]:
            self.data.drop(self.data.index[0], axis=0, inplace=True)
            self.data = pd.concat([self.data, other.data])
        else:
            self.data.update(other.data)
            self.data = self.data.astype(other.data.dtypes)
        self._time_updated = pd.Timestamp.utcnow()
