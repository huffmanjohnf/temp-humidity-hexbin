import pandas as pd
import seaborn as sns


def hexbin_plt(df: pd.DataFrame, sp_cool: float = 72.0, sp_heat: float = 68.0, sp_humi: float = 55.0):
    hexbin = sns.jointplot(
        x="Temperature",
        y="Humidity",
        data=df,
        kind="hex",
        height=6,
        ratio=15,
        space=0,
        edgecolor="w",
        xlim=(64, 76),
        ylim=(45, 65),
        color="k",
    )

    y0, y1 = hexbin.ax_joint.get_ylim()
    hexbin.ax_joint.plot([sp_cool, sp_cool], [y0, sp_humi], ":k")
    hexbin.ax_joint.plot([sp_heat, sp_heat], [y0, sp_humi], ":k")
    hexbin.ax_joint.plot([sp_heat, sp_cool], [sp_humi, sp_humi], ":k")
    hexbin.set_axis_labels("Temperature (\N{DEGREE SIGN}F)", "Humidity (Dew Point, \N{DEGREE SIGN}F)")
    return hexbin
