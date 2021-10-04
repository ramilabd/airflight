from datetime import datetime

from .parser_xml import FILE_PATH, get_xml_tree


def get_all_flights():
    """Get list of all flights with total time flight.

    Returns:
        list: list of flights, each flight is represented by a dictionary.
    """
    root = get_xml_tree(FILE_PATH).getroot()
    all_flights = []

    for Flights in root.xpath('//OnwardPricedItinerary/Flights'):
        routs = {}
        order = 0

        for Flight in Flights.iter('Flight'):
            flight = {}
            order += 1

            for elem in Flight.iter('*'):
                if elem.tag in {'Flight', 'WarningText', 'FareBasis',
                            'NumberOfStops', 'Class', 'TicketType'
                }:
                    continue
                tag = elem.tag
                text = elem.text
                flight[tag] = text

            routs['flight_{}'.format(order)] = flight

        currency = Flights.find('../../Pricing').attrib['currency']
        price = Flights.find(
            '../../Pricing/ServiceCharges[@ChargeType="TotalAmount"]'
        ).text
        routs['Price'] = dict(TicketPrice=price, Currency=currency)

        all_flights.append(routs)

    return list(map(add_total_travel_time, all_flights))


def add_total_travel_time(flight, str_time=False):
    """Calculate and added total time of the flight.

    Args:
        flight (dict): flight (route), is represented by a dictionary.
        str_time (bool, optional): adds total time as a string or
            object datetime. Defaults to False.

    Returns:
        dict: flight with added total time.
    """
    departure_time = flight['flight_1']['DepartureTimeStamp']

    if 'flight_2' in flight:
        arrival_time = flight['flight_2']['ArrivalTimeStamp']
    else:
        arrival_time = flight['flight_1']['ArrivalTimeStamp']

    time_delta = (datetime.strptime(arrival_time, '%Y-%m-%dT%H%M') -
        datetime.strptime(departure_time, '%Y-%m-%dT%H%M'))
    flight['TotalTravelTime'] = str(time_delta) if str_time else time_delta

    return flight


def get_flights_sorted_price(flights, reverse=False, flights_number=None):
    """Returns a list of flights sorted by price.

    Args:
        flights (list): list of flights, each flight is represented
            by a dictionary.
        reverse (bool, optional): defines the sorting order,
            by default to False - ascending, if True sort in descending order.
        number_flights (int, optional): the number of flights that
            need to be returned, if None returns the entire sorted list.
            Defaults to None.

    Returns:
        list: a list of flights sorted by price.
    """
    return sorted(flights, key=lambda flight: float(flight['Price']['TicketPrice']),
                reverse=reverse)[:flights_number]


def get_flights_sorted_time(flights, reverse=False, flights_number=None):
    """Returns a list of flights sorted by time.

    Args:
        flights ([type]): list of flights, each flight is represented
            by a dictionary.
        reverse (bool, optional): defines the sorting order,
            by default to False - ascending, if True sort in descending order.
        number_flights (int, optional): the number of flights that
            need to be returned, if None returns the entire sorted list.
            Defaults to None.

    Returns:
        list: a list of flights sorted by time.
    """

    return sorted(flights, key=lambda flight: flight['TotalTravelTime'],
                reverse=reverse)[:flights_number]


def get_flights_filtered_direction(source, destination):
    """Returns a list of flights sorted by directions.

    Args:
        flights (dict): list of flights, each flight is represented
            by a dictionary.
        source (str): name of city (airport) of departure.
        destination (str): name of city (airport) of arrival.

    Returns:
        list: a list of flights sorted by destination.
    """
    flights = get_all_flights()
    sorted_flights = []

    for flight in flights:
        if 'flight_2' not in flight:
            if (flight['flight_1']['Source'] == source and
                    flight['flight_1']['Destination'] == destination):
                sorted_flights.append(flight)
        else:
            if (flight['flight_1']['Source'] == source and
                    flight['flight_2']['Destination'] == destination):
                sorted_flights.append(flight)

    return sorted_flights


def get_all_routes():
    """Returns all possible routes.
    With an indication of the place of departure, transfer and destination.

    Args:
        flights (list): list all flights,
            each flight is represented by a dictionary.

    Returns:
        list: list of routes (source, transfer, destination),
            each route is represented by a dictionary.
    """
    flights = get_all_flights()
    all_routes = []

    for flight in flights:
        source = flight['flight_1']['Source']
        if 'flight_2' not in flight:
            destination = flight['flight_1']['Destination']
            all_routes.append({'Source': source, 'Destination': destination})
        else:
            transfer = flight['flight_1']['Destination']
            destination = flight['flight_2']['Destination']
            all_routes.append({'Source': source, 'Transfer': transfer, 'Destination': destination})

    return all_routes


def get_optimal_route(source, destination, flights_number=5):
    """Returns optimal flight routes (by time and price).

    Args:
        flights (list): list of flights, each flight is represented
            by a dictionary.
        source (str): name of city (airport) of departure.
        destination (str): name of city (airport) of arrival.
        number_flights (int, optional): the number of flights that
            need to be returned. By default, 5.

    Returns:
        list: a list of optimal flights (by time and price).
    """
    flights = get_all_flights()
    filtered_flight_direction = get_flights_filtered_direction(
        source, destination
    )

    mark = 1
    for flight in filtered_flight_direction:
        flight['mark'] = mark
        mark += 1

    sorted_flight_time = get_flights_sorted_time(filtered_flight_direction)
    sorted_flight_price = get_flights_sorted_price(filtered_flight_direction)

    flight_weights = []
    for flight in filtered_flight_direction:
        mark = flight['mark']
        index = filtered_flight_direction.index(flight)
        for flight_in_time in sorted_flight_time:
            if mark == flight_in_time['mark']:
                index_in_time = sorted_flight_time.index(flight_in_time)
            for flight_in_price in sorted_flight_price:
                if mark == flight_in_price['mark']:
                    index_in_price = sorted_flight_price.index(flight_in_price)
        flight_weight = index, index_in_time + index_in_price
        flight_weights.append(flight_weight)

    sorted_flight_weights = sorted(flight_weights, key=lambda item: item[1])

    optimal_route = []
    for index, _ in sorted_flight_weights[:flights_number]:
        optimal_route.append(filtered_flight_direction[index])

    return optimal_route


def formatting_time(flights):
    for flight in flights:
        flight['TotalTravelTime'] = str(flight['TotalTravelTime'])

    return flights