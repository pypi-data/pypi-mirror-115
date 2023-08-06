from flight_routes.json_models.flight_json_model import FlightJsonModel


class PlanJsonModel:
    def __init__(self, flights: list[FlightJsonModel], bags_allowed: int, bags_count: int, destination: str, origin: str,
                 total_price: float, travel_time: str):
        self.flights = flights
        self.bags_allowed = bags_allowed
        self.bags_count = bags_count
        self.destination = destination
        self.origin = origin
        self.total_price = total_price
        self.travel_time = travel_time
