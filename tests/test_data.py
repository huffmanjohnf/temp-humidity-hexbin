import io

import numpy as np
import pandas as pd
import pytest

from temp_humidity_hexbin.data import join, load_data, rh2dp


@pytest.fixture(scope="module")
def temperature_string_io() -> io.StringIO:
    temperature_string_io = io.StringIO()
    temperature_string_io.write(
        "\ufeffDateTime,RawValue,DisplayValue\r\n"
        "5/31/20 23:01,71.825,71.8°F\r\n"
        "5/31/20 23:03,71.775,71.8°F\r\n"
        "5/31/20 23:05,71.65,71.7°F\r\n"
        "5/31/20 23:07,71.675,71.7°F\r\n"
        "5/31/20 23:09,71.65,71.7°F\r\n"
    )
    return temperature_string_io


@pytest.fixture(scope="module")
def temperature_df() -> pd.DataFrame:
    temperature_df = pd.DataFrame(
        {
            "DateTime": ["5/31/20 23:01", "5/31/20 23:03", "5/31/20 23:05", "5/31/20 23:07", "5/31/20 23:09"],
            "RawValue": [71.825, 71.775, 71.65, 71.675, 71.65],
        }
    )
    return temperature_df


@pytest.fixture(scope="module")
def humidity_df() -> pd.DataFrame:
    humidity_df = pd.DataFrame(
        {
            "DateTime": [
                "5/31/20 20:03",
                "5/31/20 23:05",
                "5/31/20 23:07",
                "5/31/20 23:09",
                "5/31/20 23:09",
                "5/31/20 23:01",
            ],
            "RawValue": [38.8, 39.7, np.nan, 40.3, 40.3, 38.7],
        }
    )
    return humidity_df


def test_load_data(temperature_string_io, temperature_df):
    loaded = load_data(temperature_string_io)
    assert loaded.equals(temperature_df)


def test_join(temperature_df, humidity_df, joined_df):
    """
    Ensure joined datasets are:
         - sorted by timestamp
         - np.nan and duplicates removed
         - timestamps are reindexed no more than 1 minute apart
    """
    dfs = [
        temperature_df.rename(columns={"RawValue": "Temperature"}),
        humidity_df.rename(columns={"RawValue": "Humidity"}),
    ]
    check = join(dfs)
    assert check.equals(joined_df)


@pytest.mark.parametrize(
    "temperature, relative_humidity, dew_point",
    [(38.0, 20.0, 0.0), (68.0, 50.0, 49.0), (105.0, 60.0, 88.0)],
)
def test_rh2dp(temperature: float, relative_humidity: float, dew_point: float):
    assert dew_point == np.round(rh2dp(temperature, relative_humidity), 0)
