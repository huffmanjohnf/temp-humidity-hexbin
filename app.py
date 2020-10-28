import pandas as pd
import streamlit as st

st.title("Temperature vs. Humidity Hexbin")


@st.cache
def load_data(file_data):
    file_data.seek(0)
    return pd.read_csv(file_data)


temperature_file = st.file_uploader("Upload temperature data file", type=["csv"])
humidity_file = st.file_uploader("Upload himidity data file", type=["csv"])
humidity_type = st.selectbox("Select the type of humidity data:", ["Dew Point", "Relative Humidity"])

if not humidity_file or not humidity_file or not humidity_type:
    st.stop()

df_t = load_data(temperature_file)
df_h = load_data(humidity_file)
