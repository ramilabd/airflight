# -*- coding: utf8 -*-
"""Data analysis module."""


from datetime import datetime
from functools import lru_cache

from airflight.parser_xml import FILE_PATH, get_xml_tree


def get_all_flights():
    """Get list of all flights with total time flight.

    Returns:
        list: list of flights, each flight is represented by a dictionary.
    """
    root = get_xml_tree(FILE_PATH).getroot()
    all_flights = []

    for flights in root.xpath('//OnwardPricedItinerary/Flights'):
        all_flights.append(get_routes(flights))

    return list(map(add_total_travel_time, all_flights))


def get_routes(flights):
    """Return routes from flights.

    Args:
        flights (object of class 'lxml.etree._Element'): an object containing
            a description of flights. every flight is a "Flight" tag.

    Returns:
        dict: "FLight" tags are generated in the routes dictionary.
    """
    routes = {}
    order = 0

    for flight in flights.iter('Flight'):
        route = {}
        order += 1

        for elem in flight.iter('*'):
            route[elem.tag] = elem.text

        routes['flight_{0}'.format(order)] = route

        routes['Price'] = {
            'TicketPrice': flights.find(
                '../../Pricing/ServiceCharges[@ChargeType="TotalAmount"]',
            ).text,
            'Currency': flights.find('../../Pricing').attrib['currency'],
        }

    return routes


def add_total_travel_time(flight, str_time=False):
    """Calculate and added total time of the flight.

    Args:
        flight (dict): flight (route), is represented by a dictionary.
            str_time (bool, optional): adds total time as a string or
            object datetime. Defaults to False.
        str_time (bool): object representation "time delta",
            if True then as a string, if False then as a object
            of type datetime.timedelta.

    Returns:
        dict: flight with added total time.
    """
    departure_time = flight.get('flight_1').get('DepartureTimeStamp')

    if flight.get('flight_2'):
        arrival_time = flight.get('flight_2').get('ArrivalTimeStamp')
    else:
        arrival_time = flight.get('flight_1').get('ArrivalTimeStamp')

    time_delta = datetime.strptime(
        arrival_time, '%Y-%m-%dT%H%M',
    ) - datetime.strptime(departure_time, '%Y-%m-%dT%H%M')

    flight['TotalTravelTime'] = str(time_delta) if str_time else time_delta

    return flight


def get_flights_sorted_price(flights, reverse=False):
    """Return a list of flights sorted by price.

    Args:
        flights (list): list of flights, each flight is represented
            by a dictionary.
        reverse (bool, optional): defines the sorting order,
            by default to False - ascending, if True sort in descending order.

    Returns:
        list: a list of flights sorted by price.
    """
    return sorted(
        flights,
        key=lambda flight: float(flight['Price']['TicketPrice']),
        reverse=reverse,
    )


def get_flights_sorted_time(flights, reverse=False):
    """Return a list of flights sorted by time.

    Args:
        flights ([type]): list of flights, each flight is represented
            by a dictionary.
        reverse (bool, optional): defines the sorting order,
            by default to False - ascending, if True sort in descending order.

    Returns:
        list: a list of flights sorted by time.
    """
    return sorted(
        flights,
        key=lambda flight: flight['TotalTravelTime'],
        reverse=reverse,
    )


@lru_cache
def get_flights_filtered_direction(source, destination):
    """Return a list of flights sorted by directions.

    Args:
        source (str): name of city (airport) of departure.
        destination (str): name of city (airport) of arrival.

    Returns:
        list: a list of flights sorted by destination.
    """
    flights = get_all_flights()
    filtered_flights = []

    for flight in flights:
        source_in_flight = flight.get('flight_1').get('Source')

        if flight.get('flight_2'):
            second_flight = flight.get('flight_2')
        else:
            second_flight = flight.get('flight_1')

        if source_in_flight == source:
            if second_flight.get('Destination') == destination:
                filtered_flights.append(flight)

    return filtered_flights


def get_all_routes():
    """Return all possible routes.

        With an indication of the place of departure, transfer and destination.

    Returns:
        list: list of routes (source, transfer, destination),
            each route is represented by a dictionary.
    """
    flights = get_all_flights()
    all_routes = []

    for flight in flights:
        source = flight['flight_1']['Source']

        if flight.get('flight_2') is None:
            destination = flight['flight_1']['Destination']
            all_routes.append({'Source': source, 'Destination': destination})
        else:
            destination = flight['flight_2']['Destination']
            all_routes.append({
                'Source': source,
                'Transfer': flight['flight_1']['Destination'],
                'Destination': destination,
            })

    return all_routes


@lru_cache
def get_optimal_route(source, destination, max_count_flight=10):
    """Return optimal flight routes (by time and price).

    Args:
        source (str): name of city (airport) of departure.
        destination (str): name of city (airport) of arrival.

    Returns:
        list: a list of optimal flights (by time and price).
    """
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

    for index, _ in sorted_flight_weights[:max_count_flight]:
        optimal_route.append(filtered_flight_direction[index])

    return optimal_route


def formatting_time(flights):
    for flight in flights:
        flight['TotalTravelTime'] = str(flight['TotalTravelTime'])

    return flights
