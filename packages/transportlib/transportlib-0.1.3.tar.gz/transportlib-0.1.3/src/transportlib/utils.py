import os
import pandas as pd
import logging
from pathlib import Path


def get_from_env(
        curr_val,
        env_key: str,
        default_val,
):
    if curr_val is None:
        return os.getenv(env_key, default_val)
    else:
        return curr_val


def dump_dataframe_as_csv(
        dataframe: pd.DataFrame,
        csv_file_path,
):

    logging.info('Display dataframe')
    logging.info(dataframe)

    if csv_file_path.exists():
        logging.info(f"deleting old file {csv_file_path}")
        csv_file_path.unlink()

    dataframe.to_csv(csv_file_path, index=False)

    return dataframe
