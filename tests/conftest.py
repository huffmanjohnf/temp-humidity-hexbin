import pandas as pd
import pytest


@pytest.fixture(scope="module")
def joined_df() -> pd.DataFrame:
    joined_df = pd.DataFrame.from_dict(
        {
            "5/31/20 23:01": [71.825, 38.7],
            "5/31/20 23:05": [71.65, 39.7],
            "5/31/20 23:09": [71.65, 40.3],
        },
        orient="index",
        columns=["Temperature", "Humidity"],
    )
    joined_df.index.name = "DateTime"
    return joined_df
