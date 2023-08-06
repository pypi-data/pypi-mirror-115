from datetime import datetime


class Flight:
    def __init__(self, flight_no, origin, destination, departure, arrival, base_price, bag_price, bags_allowed):
        self.flight_no = flight_no
        self.origin = origin
        self.destination = destination
        self.departure_timestamp = datetime.strptime(departure, "%Y-%m-%dT%H:%M:%S").timestamp()
        self.departure = departure
        self.arrival_timestamp = datetime.strptime(arrival, "%Y-%m-%dT%H:%M:%S").timestamp()
        self.arrival = arrival
        self.base_price = base_price
        self.bag_price = bag_price
        self.bags_allowed = bags_allowed
        self.unique_flight_no = self.flight_no + '|' + str(self.departure)
