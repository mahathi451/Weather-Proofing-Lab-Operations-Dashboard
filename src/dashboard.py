import streamlit as st
import pandas as pd
from utils.sensor_interface import LabSensorClient
from utils.config_loader import load_config

config = load_config()
sensor_client = LabSensorClient(config['sensor_api'])

st.set_page_config(page_title="Lab Environment Monitor", layout="wide")

def display_metrics():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Temperature", f"{sensor_client.get_temperature()}°C", 
                 delta="-1.2°C/hr" if sensor_client.temp_decreasing() else "")
    with col2:
        st.metric("Humidity", f"{sensor_client.get_humidity()}%")
    with col3:
        st.metric("Pressure", f"{sensor_client.get_pressure()} hPa")

def show_historical_data():
    hist_data = sensor_client.get_historical(days=7)
    st.line_chart(hist_data.set_index('timestamp'))

def main():
    st.title("Laboratory Environmental Monitoring System")
    display_metrics()
    show_historical_data()
    
    with st.expander("Export Data"):
        st.download_button("Download CSV", 
                          sensor_client.get_historical().to_csv(),
                          "lab_environment.csv")

if __name__ == "__main__":
    main()
