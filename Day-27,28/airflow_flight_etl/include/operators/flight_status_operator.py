from airflow.models import BaseOperator
from include.hooks.flight_api_hook import FlightAPIHook

class FlightStatusOperator(BaseOperator):
    template_fields = ["airport"]

    def __init__(self, airport, **kwargs):
        super().__init__(**kwargs)
        self.airport = airport

    def execute(self, context):
        hook = FlightAPIHook()
        self.log.info(f"Fetching data for airport: {self.airport}")
        data = hook.get_flights()
        return data
