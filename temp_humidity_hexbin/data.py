import io
from typing import List

import numpy as np
import pandas as pd
import streamlit as st


@st.cache
def load_data(file_data: io.StringIO):
    file_data.seek(0)
    return pd.read_csv(file_data, usecols=["DateTime", "RawValue"])


def preprocess(df: pd.DataFrame):
    df["DateTime"] = pd.to_datetime(df["DateTime"].str.replace("/", "-"))
    df.drop_duplicates(subset="DateTime", inplace=True)
    df = df.set_index("DateTime").sort_index()
    return df


def join(dfs: List[pd.DataFrame]):
    dfs = [preprocess(df) for df in dfs]
    dfs[1] = dfs[1].reindex(dfs[0].index, method="nearest", tolerance=pd.Timedelta(value=1, unit="m"))
    df = dfs[0].join(dfs[1], how="inner")
    return df.dropna(axis=0)


def rh2dp(tf: float = 72.0, rh: float = 55.0) -> float:
    t_c = (tf - 32) / 1.8  # convert to Celcius

    rh = max([0.2, (rh / 100)])
    ln_rh = np.log(rh)
    dp_c = 243.04 * (ln_rh + ((17.625 * t_c) / (243.04 + t_c))) / (17.625 - ln_rh - ((17.625 * t_c) / (243.04 + t_c)))

    dp_f = (1.8 * dp_c) + 32  # convert to Fahrenheit
    return dp_f
