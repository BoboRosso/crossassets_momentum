import pandas as pd
import re


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
