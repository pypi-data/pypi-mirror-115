import csv
import operator

from flight_routes.chain import Chain
from flight_routes.flight import Flight
from flight_routes.exporter import to_json

MIN_LAYOVER = 60 * 60
MAX_LAYOVER = 6 * 60 * 60


def __is_flight_in_time_bounds(chain, flight):
    if flight.origin == chain.last_visited_target:
        return True

    if chain.time + MIN_LAYOVER > flight.departure_timestamp:
        return False

    if flight.departure_timestamp > chain.time + MAX_LAYOVER:
        chain.set_as_dead()
        return False

    return True


def __init_flights_from_csv(csv_path, origin, destination, bags, ret):
    with open(csv_path, newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        next(csv_data)
        flight_dict = {}
        for row in csv_data:
            flight = Flight(*row)
            if not ret and (flight.destination == origin or flight.origin == destination):
                continue
            if bags > 0 and int(flight.bags_allowed) < bags:
                continue

            flight_dict[flight.unique_flight_no] = flight

        return flight_dict


def search(csv_path, origin, destination, bags, ret):
    flight_dict = __init_flights_from_csv(csv_path, origin, destination, bags, ret)

    sorted_flights = sorted(flight_dict.values(), key=operator.attrgetter('departure_timestamp'))

    plans = __find_available_flight_plans(origin, destination, sorted_flights, ret)

    return to_json(plans, flight_dict, origin, destination, bags)


def __find_available_flight_plans(origin, destination, sorted_flights, with_return):
    destination_list = [destination]
    if with_return:
        destination_list.append(origin)

    chains_indexed_by_airports = {origin: [Chain(0, {origin}, [], destination_list, origin), ]}

    finished_plan_chains = []

    for flight in sorted_flights:
        if flight.origin in chains_indexed_by_airports:
            chains_indexed_by_airports[flight.origin] = __remove_dead_chains(chains_indexed_by_airports[flight.origin])

            for chain in chains_indexed_by_airports[flight.origin]:

                if not __is_flight_in_time_bounds(chain, flight) or flight.destination in chain.visited_airports:
                    continue

                new_chain = chain.create_new_chain_from_flight(flight)

                if flight.destination == chain.destination_list[0]:
                    if len(chain.destination_list) == 1:
                        finished_plan_chains.append(new_chain)
                        continue
                    new_chain.set_next_target_in_plan()

                chains_indexed_by_airports.setdefault(flight.destination, []).append(new_chain)

    return finished_plan_chains


def __remove_dead_chains(chains_indexed_by_airports):
    return list(
        filter(lambda c: not c.dead, chains_indexed_by_airports))
