from airflow.providers.http.hooks.http import HttpHook

class FlightAPIHook(HttpHook):
    def __init__(self):
        super().__init__(method="GET", http_conn_id="opensky_api")

    def get_flights(self):
        endpoint = "states/all"
        response = self.run(endpoint)
        return response.json().get("states", [])
