# -*- coding: utf8 -*-
"""Data analysis module."""


from functools import lru_cache

from airflight.auxiliary_func import add_total_travel_time, get_flight_weights
from airflight.parser_xml import FILE_PATH, get_xml_tree


def get_all_flights():
    """Get list of all flights with total time flight.

    Returns:
        list: list of flights, each flight is represented by a dictionary.
    """
    root = get_xml_tree(FILE_PATH).getroot()
    all_flights = []

    for flights in root.xpath('//OnwardPricedItinerary/Flights'):
        all_flights.append(get_route(flights))

    return list(map(add_total_travel_time, all_flights))


def get_route(flights):
    """Return route from flights.

    Args:
        flights (object of class 'lxml.etree._Element'): an object containing
            a description of flights. every flight is a "Flight" tag.

    Returns:
        dict: "FLight" tags are generated in the route dictionary.
    """
    route = {}
    order = 0

    for flight in flights.iter('Flight'):
        flight_direction = {}
        order += 1

        for elem in flight.iter('*'):
            flight_direction[elem.tag] = elem.text

        route['flight_{0}'.format(order)] = flight_direction

        route['Price'] = {
            'TicketPrice': flights.find(
                '../../Pricing/ServiceCharges[@ChargeType="TotalAmount"]',
            ).text,
            'Currency': flights.find('../../Pricing').attrib['currency'],
        }

    return route


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
