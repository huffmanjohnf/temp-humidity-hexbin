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

df = join(dfs=[df_t, df_h])
if humidity_type == "Relative Humidity":
    df = rh2dp(df)

hexbin = hexbin_plt(df)
st.pyplot(hexbin)
