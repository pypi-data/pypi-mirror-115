class Chain:
    def __init__(self, time, airport_dict, flight_list, destination_list, last_visited_target):
        self.time = time
        self.visited_airports = airport_dict
        self.flight_list = flight_list
        self.dead = False
        self.destination_list = destination_list
        self.last_visited_target = last_visited_target

    def create_new_chain_from_flight(self, flight):
        return Chain(flight.arrival_timestamp, self.visited_airports | {flight.destination},
                     self.flight_list + [flight.unique_flight_no], self.destination_list.copy(),
                     self.last_visited_target)

    def set_next_target_in_plan(self):
        actual_destination = self.destination_list.pop(0)
        self.visited_airports = {actual_destination}
        self.last_visited_target = actual_destination

    def set_as_dead(self):
        self.dead = True
