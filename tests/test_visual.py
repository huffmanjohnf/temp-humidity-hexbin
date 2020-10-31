import pytest

from temp_humidity_hexbin.visual import hexbin_plt


@pytest.mark.parametrize(
    "sp_cool, sp_heat, sp_humi",
    [(72.0, 68.0, 55.0), (76.0, 64.0, 60.0), (72.5, 68.4, 55.6)],
)
def test_hexbin_plt(joined_df, sp_cool, sp_heat, sp_humi):
    _ = hexbin_plt(joined_df, sp_cool, sp_heat, sp_humi)
