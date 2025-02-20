# Lab Environmental Monitoring Dashboard

Real-time monitoring system for laboratory conditions with data logging and alert capabilities.

## Features
- Real-time temperature/humidity/pressure monitoring
- 7-day historical trend visualization
- CSV data export functionality
- Configurable alert thresholds

## Installation
1. Clone repository:
git clone https://github.com/yourusername/lab-dashboard.git
cd lab-dashboard
text
2. Install dependencies:
pip install -r requirements.txt
text
3. Configure API credentials in `config/lab_config.yaml`

## Usage
streamlit run src/dashboard.py
text

## Configuration
Modify `lab_config.yaml`:
sensor_api:
endpoint: "https://api.lab-sensors.com/v2"
key: "your_api_key_here"
alert_thresholds:
temperature:
min: 18
max: 25
humidity:
min: 30
max: 60
