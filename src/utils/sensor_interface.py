import requests
import time

class LabSensorClient:
    def __init__(self, api_config):
        self.base_url = api_config['endpoint']
        self.api_key = api_config['key']
        self.cache = {}
        
    def _make_request(self, endpoint):
        if time.time() - self.cache.get(endpoint, {}).get('timestamp', 0) < 60:
            return self.cache[endpoint]['data']
            
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        
        self.cache[endpoint] = {
            'data': response.json(),
            'timestamp': time.time()
        }
        return self.cache[endpoint]['data']
    
    def get_temperature(self):
        return self._make_request('temperature')['value']
    
    def get_humidity(self):
        return self._make_request('humidity')['value']
    
    def get_historical(self, days=7):
        return pd.DataFrame(self._make_request(f'history?days={days}'))
