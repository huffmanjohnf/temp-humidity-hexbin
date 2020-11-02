import pytest

from temp_humidity_hexbin.visual import hexbin_plt


@pytest.mark.parametrize(
    "sp_cool, sp_heat, sp_humi, xlim, ylim",
    [
        (72.0, 68.0, 55.0, (64, 76), (40, 65)),
        (76.0, 64.0, 60.0, (63.5, 72.5), (50.5, 60.5)),
        (72.5, 68.4, 55.6, None, None),
        (72.0, 68.0, 55.0, None, (45, 65)),
        (72.0, 68.0, 55.0, None, None),
    ],
)
def test_hexbin_plt(joined_df, sp_cool, sp_heat, sp_humi, xlim, ylim):
    _ = hexbin_plt(joined_df, sp_cool, sp_heat, sp_humi, xlim, ylim)


def test_all_defaults(joined_df):
    _ = hexbin_plt(joined_df)
