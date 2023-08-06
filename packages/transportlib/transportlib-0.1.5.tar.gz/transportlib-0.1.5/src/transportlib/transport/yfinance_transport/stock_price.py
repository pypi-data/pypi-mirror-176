import datetime
import logging
import traceback
from pathlib import Path
from typing import List, Optional
import yfinance as yf
import pandas as pd
from transportlib.transport import BaseTransport

from transportlib.utils import dump_dataframe_as_csv, safe_convert_iso_str_to_datetime


class HistoricalStockPriceTransport(BaseTransport):

    def __init__(
            self,
            tickers: Optional[List[str]] = None,
            *args,
            **kwargs,
    ):
        super(HistoricalStockPriceTransport, self).__init__(*args, **kwargs)

        self.start_datetime = safe_convert_iso_str_to_datetime(self.watermark_val_prev)
        self.end_datetime = safe_convert_iso_str_to_datetime(self.watermark_val_curr)

        if tickers is None:
            logging.info("Tickers set to None. Running all available HK tickers.")
            tickers = [f"{str(i).rjust(4, '0')}.hk" for i in range(1, 10001)]

        self.tickers = tickers

    def run(self):
        for ticker in self.tickers:
            logging.info(f'running ticker {ticker}')

            try:
                hist_df: pd.DataFrame = yf.download(
                tickers=ticker,
                start=self.start_datetime,
                end=self.end_datetime,
            )
            except KeyboardInterrupt as e:
                # stop and end
                logging.error(traceback.format_exc())
                break
            except Exception as e:
                # Can throw all sorts of errors
                logging.error(traceback.format_exc())
                continue

            else:

                hist_df = hist_df.reset_index()
                hist_df.insert(0, 'ticker', ticker)
                hist_df = hist_df.rename(
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
                hist_df['lib'] = 'yfinance'
                hist_df['lib'] = 'yfinance'
                hist_df['lib_called_at'] = datetime.datetime.utcnow()

                hist_df = pd.concat([hist_df, hist_df])
                dump_dataframe_as_csv(dataframe=hist_df, csv_file_path=self.csv_file_path)

