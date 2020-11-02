import streamlit as st

from temp_humidity_hexbin.data import join, load_data, rh2dp
from temp_humidity_hexbin.visual import hexbin_plt

st.title("Temperature vs. Humidity Hexbin")

temperature_file = st.file_uploader("Upload temperature data file", type=["csv"])
humidity_file = st.file_uploader("Upload himidity data file", type=["csv"])
humidity_type = st.selectbox("Select the type of humidity data:", ["Select", "Dew Point", "Relative Humidity"])

if not humidity_file or not humidity_file or humidity_type == "Select":
    st.stop()

df_t = load_data(temperature_file).rename(columns={"RawValue": "Temperature"})
df_h = load_data(humidity_file).rename(columns={"RawValue": "Humidity"})

col1, col2 = st.beta_columns(2)

with col1:
    sp_heat = st.slider("Heating Set Point (\N{DEGREE SIGN}F)", 64.0, 72.0, 68.0, 0.5)
    sp_cool = st.slider("Cooling Set Point (\N{DEGREE SIGN}F)", 68.0, 76.0, 72.0, 0.5)
    sp_humi = st.slider("Humidity Set Point (Dew Point, \N{DEGREE SIGN}F)", 45.0, 65.0, 55.0, 0.5)

with col2:
    df = join(dfs=[df_t, df_h])
    if humidity_type == "Relative Humidity":
        df["Humidity"] = [rh2dp(row["Temperature"], row["Humidity"]) for _, row in df.iterrows()]

    hexbin = hexbin_plt(df, sp_cool, sp_heat, sp_humi)
    st.pyplot(hexbin)
