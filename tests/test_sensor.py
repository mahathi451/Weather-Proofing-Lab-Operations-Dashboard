import pytest
from unittest.mock import Mock
from src.utils.sensor_interface import LabSensorClient
import time
import pandas as pd

@pytest.fixture
def mock_sensor_api():
    api = Mock()
    api.get.return_value.json.return_value = {
        "temperature": {"value": 22.5, "timestamp": 1620000000},
        "humidity": {"value": 45.0, "timestamp": 1620000000},
        "history": [
            {"timestamp": "2023-05-01T00:00", "temp": 22.0, "humidity": 45},
            {"timestamp": "2023-05-01T01:00", "temp": 21.8, "humidity": 46}
        ]
    }
    return api

def test_sensor_caching(requests_mock):
    # Mock API endpoint
    requests_mock.get(
        "https://api.lab-sensors.com/v2/temperature",
        json={"value": 22.5}
    )
    
    client = LabSensorClient({
        "endpoint": "https://api.lab-sensors.com/v2",
        "key": "test_key",
        "cache_ttl": 60
    })
    
    # First call - hits API
    temp = client.get_temperature()
    assert temp == 22.5
    assert requests_mock.call_count == 1
    
    # Second call within TTL - uses cache
    client.get_temperature()
    assert requests_mock.call_count == 1
    
    # Force cache expiration
    time.sleep(61)
    client.get_temperature()
    assert requests_mock.call_count == 2

def test_historical_data_formatting(mock_sensor_api):
    client = LabSensorClient({})
    client._make_request = mock_sensor_api.get
    
    hist_data = client.get_historical(days=7)
    assert isinstance(hist_data, pd.DataFrame)
    assert list(hist_data.columns) == ["timestamp", "temp", "humidity"]
    assert len(hist_data) == 2

def test_error_handling(requests_mock):
    requests_mock.get(
        "https://api.lab-sensors.com/v2/temperature",
        status_code=500
    )
    
    client = LabSensorClient({
        "endpoint": "https://api.lab-sensors.com/v2",
        "key": "test_key"
    })
    
    with pytest.raises(requests.HTTPError):
        client.get_temperature()
