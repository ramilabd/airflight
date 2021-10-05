# -*- coding: utf8 -*-
"""Sorting verification module."""


from airflight.data_analysis import (
    get_flights_filtered_direction,
    get_flights_sorted_price,
    get_flights_sorted_time,
)


def is_correct_sort_by_price(flights, reverse: bool):
    """Check whether the sorting is correct by price.

    Args:
        flights (list): list of flights, each flight is represented
            by a dictionary.
        reverse (bool): determines the sorting order of the function being
            checked, if False - ascending, if True - sorting in descending
            order.

    Returns:
        bool: True if the sorting is correct, False if the sorting is incorrect
    """
    is_correct_sort = True
    sort_flights_by_price = get_flights_sorted_price(flights, reverse=reverse)
    current_price = float(sort_flights_by_price[0]['Price']['TicketPrice'])

    for flight in sort_flights_by_price:
        next_price = float(flight['Price']['TicketPrice'])
        if reverse:
            if current_price < next_price:
                is_correct_sort = False
        elif current_price > next_price:
            is_correct_sort = False
        current_price = next_price

    return is_correct_sort


def is_correct_sorting_by_time(flights, reverse: bool):
    """Check whether the sorting is correct by time.

    Args:
        flights (list): list of flights, each flight is represented
            by a dictionary.
        reverse (bool): determines the sorting order of the function being
            checked, if False - ascending, if True - sorting in descending
            order.

    Returns:
        bool: True if the sorting is correct, False if the sorting is incorrect
    """
    is_correct_sort = True
    sort_flights_by_time = get_flights_sorted_time(flights, reverse=reverse)

    index = 0
    while is_correct_sort and index + 1 < len(sort_flights_by_time):
        prev_time = sort_flights_by_time[index]['TotalTravelTime']
        next_time = sort_flights_by_time[index + 1]['TotalTravelTime']
        if reverse:
            if prev_time < next_time:
                is_correct_sort = False
        elif prev_time > next_time:
            is_correct_sort = False
        index += 1

    return is_correct_sort


def is_correct_filtered_by_direction(all_flights, all_routes):
    """Check whether filtering by source and destination.

    Args:
        all_flights (fixture): fixture function that returns a function that,
            when called, returns a list of flights, where each flight is
            represented by a dictionary.
        all_routes (fixture): fixture function that returns a function that,
            when called, returns a list of routes, where each route is
            represented by a dictionary {source, transfer, destination}.

    Returns:
        bool: True if the filtering is correct, False if the filtering
            is incorrect.
    """
    is_correct_filtered = True
    for route in all_routes():
        sort_flights_by_source_destination = get_flights_filtered_direction(
            route['Source'],
            route['Destination'],
        )
        count_routes = 0
        for flight in all_flights:
            if flight in sort_flights_by_source_destination:
                count_routes += 1
        is_correct_filtered = count_routes == len(
            sort_flights_by_source_destination,
        )

    return is_correct_filtered
