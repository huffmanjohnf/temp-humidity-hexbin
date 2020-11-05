import streamlit as st

from temp_humidity_hexbin.data import join, load_data, rh2dp
from temp_humidity_hexbin.visual import hexbin_plt

st.title("Temperature vs. Humidity Hexbin Plot")

st.sidebar.write(
    "See [README.md](https://github.com/huffmanjohnf/temp-humidity-hexbin/blob/main/README.md) for overview."
)
st.sidebar.subheader("Upload data files:")
temperature_file = st.sidebar.file_uploader("Upload temperature data file", type=["csv"])
humidity_file = st.sidebar.file_uploader("Upload humidity data file", type=["csv"])
if not temperature_file or not humidity_file:
    st.stop()

st.sidebar.subheader("Specify uploaded humidity type:")
humidity_type = st.sidebar.selectbox(
    "", ["Select", "Dew Point", "Relative Humidity (0-10V)", "Relative Humidity (0-100%)"]
)
if humidity_type == "Select":
    st.stop()

df_t = load_data(temperature_file).rename(columns={"RawValue": "Temperature"})
df_h = load_data(humidity_file).rename(columns={"RawValue": "Humidity"})

col1, col2 = st.beta_columns([2, 3])

with col1:
    plt_params = {}

    plt_params["sp_heat"] = st.slider("Heating Set Point (\N{DEGREE SIGN}F)", 64.0, 72.0, 68.0, 0.5)
    plt_params["sp_cool"] = st.slider("Cooling Set Point (\N{DEGREE SIGN}F)", 68.0, 76.0, 72.0, 0.5)
    plt_params["sp_humi"] = st.slider("Humidity Set Point (Dew Point, \N{DEGREE SIGN}F)", 45.0, 65.0, 55.0, 0.5)

    with st.beta_expander("Relative Humidity to Dew Point Calculator"):
        t = st.number_input("Temperature (\N{DEGREE SIGN}F)", min_value=20, max_value=100, value=72)
        rh = st.number_input("Relative Humidity (%)", min_value=20, max_value=100, value=55)
        dp = rh2dp(t, rh)
        st.write("Equivalent Dew Point: {:.1f} \N{DEGREE SIGN}F".format(dp))

    with st.beta_expander("Override Plot Window"):
        x_override = st.checkbox("Override X-axis")
        if x_override:
            x1 = st.number_input("X-axis range", min_value=20, max_value=100, value=64)
            x2 = st.number_input("", min_value=20, max_value=100, value=76)
            plt_params["xlim"] = (min([x1, x2]), max([x1, x2]))

        y_override = st.checkbox("Override Y-axis")
        if y_override:
            y1 = st.number_input("Y-axis range", min_value=20, max_value=100, value=45)
            y2 = st.number_input("", min_value=20, max_value=100, value=65)
            plt_params["ylim"] = (min([y1, y2]), max([y1, y2]))

with col2:
    df = join(dfs=[df_t, df_h])
    if humidity_type == "Relative Humidity (0-10V)":
        df["Humidity"] *= 10
    if humidity_type.startswith("Relative Humidity"):
        df["Humidity"] = [rh2dp(row["Temperature"], row["Humidity"]) for _, row in df.iterrows()]

    hexbin = hexbin_plt(df, **plt_params)
    st.pyplot(hexbin)
