from flight_routes.flight import Flight


class FlightJsonModel:
    def __init__(self, flight: Flight):
        self.flight_no = flight.flight_no
        self.origin = flight.origin
        self.destination = flight.destination
        self.departure = flight.departure
        self.arrival = flight.arrival
        self.base_price = flight.base_price
        self.bag_price = flight.bag_price
        self.bags_allowed = flight.bags_allowed
