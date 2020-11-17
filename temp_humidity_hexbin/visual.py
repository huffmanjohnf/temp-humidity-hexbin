from typing import Tuple

import pandas as pd
import seaborn as sns


def get_range(S: pd.Series):
    return (S.quantile(0.01), S.quantile(0.99))


def find_edge(considerations, how: str = "max", buffer: int = 1):
    assert how in ["min", "max"]
    if how == "min":
        return min(considerations) - buffer
    else:
        return max(considerations) + buffer


def gridsize(x_01: float, x_99: float, y_01: float, y_99: float, scale: int = 2):
    xgrid = x_99 - x_01
    ygrid = y_99 - y_01
    correction_factor = min([xgrid, ygrid])
    xgrid = max([int(xgrid * (correction_factor / xgrid) * scale), 1])
    ygrid = max([int(ygrid * (correction_factor / ygrid) * scale), 1])
    return (ygrid, xgrid)


def hexbin_plt(
    df: pd.DataFrame,
    sp_cool: float = 72.0,
    sp_heat: float = 68.0,
    sp_humi: float = 55.0,
    xlim: Tuple[int] = None,
    ylim: Tuple[int] = None,
):
    x_range = get_range(df["Temperature"])
    y_range = get_range(df["Humidity"])

    if not xlim:
        xlim = (find_edge([sp_heat, x_range[0]], "min"), find_edge([sp_cool, x_range[1]], "max"))
    if not ylim:
        ylim = (find_edge([y_range[0]], "min"), find_edge([sp_humi, y_range[1]], "max"))

    df["Temperature"] = df["Temperature"].clip(*x_range)
    df["Humidity"] = df["Humidity"].clip(*y_range)

    hexbin = sns.jointplot(
        x="Temperature",
        y="Humidity",
        data=df,
        kind="hex",
        height=6,
        ratio=15,
        space=0,
        edgecolor="w",
        xlim=xlim,
        ylim=ylim,
        joint_kws=dict(gridsize=gridsize(*x_range, *y_range)),
        color="k",
    )

    y0, y1 = hexbin.ax_joint.get_ylim()
    hexbin.ax_joint.plot([sp_cool, sp_cool], [y0, sp_humi], ":k")
    hexbin.ax_joint.plot([sp_heat, sp_heat], [y0, sp_humi], ":k")
    hexbin.ax_joint.plot([sp_heat, sp_cool], [sp_humi, sp_humi], ":k")
    hexbin.set_axis_labels("Temperature (\N{DEGREE SIGN}F)", "Humidity (Dew Point, \N{DEGREE SIGN}F)")
    return hexbin
