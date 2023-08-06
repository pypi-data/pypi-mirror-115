import json
import operator
import sys

from json_models.flight_json_model import FlightJsonModel
from json_models.plan_json_model import PlanJsonModel


def to_json(list_of_flights, indexed_flights, origin, destination, bags):
    plans = []
    for plan in list_of_flights:

        max_bags = sys.maxsize
        total_price = 0.0
        total_time = 0
        flights = []
        for flight_index in plan.flight_list:

            flight = indexed_flights[flight_index]
            flight_json = FlightJsonModel(flight)

            flights.append(flight_json)

            max_bags = min(max_bags, int(flight.bags_allowed))
            total_price += float(flight.base_price) + float(flight.bag_price) * bags
            total_time += flight.arrival_timestamp - flight.departure_timestamp

        plan = PlanJsonModel(flights, max_bags, bags, destination, origin, total_price,
                             __get_time_string(total_time))
        plans.append(plan)
    plans = sorted(plans, key=operator.attrgetter('total_price'))

    return json.dumps(plans, default=lambda o: o.__dict__, indent=4)


def __get_time_string(total_time_in_sec):
    h = int(total_time_in_sec / 60 / 60)
    m = int(total_time_in_sec / 60) - h * 60
    s = int(total_time_in_sec) - h * 60 * 60 - m * 60
    h = __pad_to_len_2(h)
    m = __pad_to_len_2(m)
    s = __pad_to_len_2(s)

    return f"{h}:{m}:{s}"


def __pad_to_len_2(var):
    if var < 10:
        return f"0{var}"
    return var
