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
def get_optimal_route(source, destination, count=10):
    """Return optimal flight routes by time and price.

    Args:
        source (str): name of city (airport) of departure.
        destination (str): name of city (airport) of arrival.
        count (int, optional): the number of flights to be returned.

    Returns:
        list: a list of optimal flights by time and price.
    """
    sort_flight_time = get_flights_sorted_time(get_flights_filtered_direction(
        source,
        destination,
    ))
    sort_flight_price = get_flights_sorted_price(get_flights_filtered_direction(
        source,
        destination,
    ))

    flight_weights = get_flight_weights(sort_flight_time, sort_flight_price)

    optimal_route = []
    for flight, _ in sorted(flight_weights, key=lambda pair: pair[1])[:count]:
        optimal_route.append(flight)

    return optimal_route


def get_flight_weights(sort_flight_time, sort_flight_price):
    """Calculate the sum of indexes of the same object in two lists.

    Args:
        sort_flight_time (list): list of flights sorted by time.
        sort_flight_price (list): list of flights sorted by price.

    Returns:
        list: a list of tuples, where each tuple is a pair -
            dictionary (flight) and the sum of the indexes of this
            dictionary in from two lists.
    """
    flight_weights = []

    for index_in_time, flight_in_time in enumerate(sort_flight_time):
        for index_in_price, flight_in_price in enumerate(sort_flight_price):
            if flight_in_time == flight_in_price:
                flight_weights.append((
                    flight_in_price,
                    index_in_time + index_in_price,
                ))

    return flight_weights


def formatting_time(flights):
    for flight in flights:
        flight['TotalTravelTime'] = str(flight['TotalTravelTime'])

    return flights
