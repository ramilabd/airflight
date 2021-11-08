# -*- coding:utf-8 -*-
"""Module auxiliary functions for data analysis."""


from datetime import datetime


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
    departure_time = flight.get('flight1').get('DepartureTimeStamp')

    if flight.get('flight2'):
        arrival_time = flight.get('flight2').get('ArrivalTimeStamp')
    else:
        arrival_time = flight.get('flight1').get('ArrivalTimeStamp')

    time_delta = datetime.strptime(
        arrival_time, '%Y-%m-%dT%H%M',
    ) - datetime.strptime(departure_time, '%Y-%m-%dT%H%M')

    flight['TotalTravelTime'] = str(time_delta) if str_time else time_delta

    return flight


def formatting_time(flights):
    """Change the representation of time in flight.

    Args:
        flights (list): list of flights, each flight is represented
            by a dictionary. Time in the dictionary is represented by an
                object "datetime".

    Returns:
        list: list of flights, each flight is represented
            by a dictionary. Time in the dictionary is represented by string
                in format '%Y-%m-%dT%H%M'.
    """
    for flight in flights:
        flight['TotalTravelTime'] = str(flight['TotalTravelTime'])

    return flights


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
