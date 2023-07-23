import pandas
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

    def t_stat_momentum(
            self,
            skip_month: int = 1,
            lookback: int = 12):
        t_stat = self.x.shift(1).rolling(11).apply(
            lambda y: sma.OLS(
                y,
                smt.tools.add_constant(
                    np.arange(y.shape[0])
                    )
                ).fit().tvalues[1]
        )
        self.momentum_measure = t_stat