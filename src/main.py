
import numpy as np
import matplotlib.pyplot as plt
from src import data_reader


def main():
    ts = data_reader.TimeSeries(
        source_file='20230715_timeseries.xlsx'
    )

    momentum = ts.data.resample('M').last().apply(np.log).shift(1).diff(11)
    ranking = momentum.rank(axis=1, ascending=False)
    weight = ranking.le(ranking.max(axis=1) / 3, axis=0)
    weight = weight.divide(weight.sum(axis=1), axis=0)

    pnl = (ts.data.resample('M').last().pct_change() * weight.shift(1)).sum(axis=1)

    (1 + pnl).cumprod().plot()
    (1 + ts.data.resample('M').last().pct_change().mean(axis=1)).cumprod().plot()