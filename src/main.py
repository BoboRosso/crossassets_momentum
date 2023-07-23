import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib; matplotlib.use('Qt5Agg')

class TimeSeries(object):
    def __init__(
            self,
            source_file: str = None,
            underlying_data: pd.DataFrame = None):

        if source_file is not None:
            self.raw_data = pd.read_excel(f"data/{source_file}")
        elif underlying_data:
            self.raw_data = underlying_data

        self.data = None
        self.setup_data()
        self.clean_data()

    def setup_data(self):
        self.data = self.raw_data
        self.data.set_index(inplace=True, keys="Date", drop=True)
        self.data.index = pd.DatetimeIndex(self.data.index)
        self.data = self.data.sort_index()
        self.data = self.data.rename(
            columns=lambda x: re.sub(r' \([LR]\d+\)', '', x))

    def clean_data(self):
        self.data = self.data.dropna(how='all')


if __name__ == 'main':
    ts = TimeSeries(
        source_file='20230715_timeseries.xlsx'
    )

    momentum = ts.data.resample('M').last().apply(np.log).shift(1).diff(11)
    ranking = momentum.rank(axis=1, ascending=False)
    weight = ranking.le(ranking.max(axis=1) / 3, axis=0)
    weight = weight.divide(weight.sum(axis=1), axis=0)

    pnl = (ts.data.resample('M').last().pct_change() * weight.shift(1)).sum(axis=1)

    (1 + pnl).cumprod().plot()
    (1 + ts.data.resample('M').last().pct_change().mean(axis=1)).cumprod().plot()