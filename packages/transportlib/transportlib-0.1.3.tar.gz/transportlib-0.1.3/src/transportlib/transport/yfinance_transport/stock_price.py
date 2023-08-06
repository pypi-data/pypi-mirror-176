import datetime
import logging
import traceback
from pathlib import Path
from typing import List, Optional
import yfinance as yf
import pandas as pd
from transportlib.transport import BaseTransport

from transportlib.utils import dump_dataframe_as_csv


class HistoricalStockPriceTransport(BaseTransport):

    def __init__(
            self,
            csv_file_path: Path,
            start_datetime: datetime.datetime,
            end_datetime: datetime.datetime,
            tickers: Optional[List[str]] = None,
    ):
        super(HistoricalStockPriceTransport, self).__init__(csv_file_path=csv_file_path)

        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

        if tickers is None:
            logging.info("Tickers set to None. Running all available HK tickers.")
            tickers = [f"{str(i).rjust(4, '0')}.hk" for i in range(1, 9999)]

        self.tickers = tickers

    def run(self):
        hist_df = pd.DataFrame()

        try:
            for ticker in self.tickers:
                logging.info(f'running ticker {ticker}')

                hist_df_new: pd.DataFrame = yf.download(
                    tickers=ticker,
                    start=self.start_datetime,
                    end=self.end_datetime,
                )

                hist_df_new = hist_df_new.reset_index()
                hist_df_new.insert(0, 'ticker', ticker)
                hist_df_new = hist_df_new.rename(
                    columns=
                    {
                        'Date': 'date',
                        'Open': 'open',
                        'High': 'high',
                        'Low': 'low',
                        'Close': 'close',
                        'Adj Close': 'adj_close',
                        'Volume': 'volume',
                    }
                )
                hist_df_new['lib'] = 'yfinance'
                hist_df_new['lib'] = 'yfinance'
                hist_df_new['lib_called_at'] = datetime.datetime.utcnow()

                hist_df = pd.concat([hist_df, hist_df_new])
        except KeyboardInterrupt as e:
            logging.error(traceback.format_exc())


        path_to_csv_file = dump_dataframe_as_csv(dataframe=hist_df, csv_file_path=self.csv_file_path)

        return path_to_csv_file
