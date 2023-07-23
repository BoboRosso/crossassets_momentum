import numpy as np
import pandas as pd
import statsmodels.tools as smt
import statsmodels.api as sma


class MomentumLib(object):
    def __init__(
            self,
            x: pd.DataFrame):
        self.momentum_measure = None
        self.x = x

    def price_momentum(
            self,
            skip_month: int = 1,
            lookback: int = 12,
            pct_change: bool = True):
        if pct_change:
            self.momentum_measure = self.x.shift(
                skip_month).pct_change(lookback - skip_month)
        else:
            self.momentum_measure = self.x.shift(
                skip_month).diff(lookback - skip_month)
        return self.momentum_measure

    def t_stat_momentum(
            self,
            skip_month: int = 1,
            lookback: int = 12):
        t_stat = self.x.shift(skip_month).rolling(lookback).apply(
            lambda y: sma.OLS(
                y,
                smt.tools.add_constant(
                    np.arange(y.shape[0])
                    )
                ).fit().tvalues[1]
        )
        self.momentum_measure = t_stat
        return self.momentum_measure


class MomentumAllocation(object):
    def __init__(
            self,
            momentum_measure: pd.DataFrame,
            long_short: bool=False,
            method: str="ew",
            n: int=3):
        self.momentum_measure = momentum_measure
        self.long_short = long_short
        self.method = method
        self.n = n
        self.ranking_df = None
        self.ranking()

    def ranking(self):
        self.ranking_df = self.momentum_measure.rank(axis=1, ascending=False)

    def allocation(self):
        if self.method == 'ew':
            if self.long_short:
                self.weight = self.ranking_df.le(
                    self.ranking_df.max(axis=1) / 3, axis=0)



