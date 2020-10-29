import io
from typing import List

import numpy as np
import pandas as pd
import streamlit as st


@st.cache
def load_data(file_data: io.StringIO):
    file_data.seek(0)
    return pd.read_csv(file_data, usecols=[0, 1])


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


def rh2dp(df: pd.DataFrame):
    rh = df["Humidity"]
    tc = (df["Temperature"] - 32) / 1.8  # convert to Celcius
    rh = np.maximum(0.2, rh / 100)
    lrh = np.log(rh)
    dp_Celcius = 243.04 * (lrh + ((17.625 * tc) / (243.04 + tc))) / (17.625 - lrh - ((17.625 * tc) / (243.04 + tc)))
    df["Humidity"] = (1.8 * dp_Celcius) + 32
    return df
