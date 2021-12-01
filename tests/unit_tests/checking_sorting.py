# -*- coding: utf8 -*-
"""Sorting verification module."""


from airflights.data_analysis import (
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


def is_correct_filtered_by_direction(all_flights, get_routes_in_parts):
    """Check whether filtering by source and destination.

    Args:
        all_flights (fixture): fixture function that returns a function that,
            when called, returns a list of flights, where each flight is
            represented by a dictionary.
        get_routes_in_parts (fixture): Returns each route from the list
            separately. Each route is represented by a dictionary,
            dictionary of the form:
            {'Source': ..., 'Transfer': ..., 'Destination': ...}.

    Returns:
        bool: True if the filtering is correct, False if the filtering
            is incorrect.
    """
    for route in get_routes_in_parts:
        sort_flights_by_source_destination = get_flights_filtered_direction(
            route['Source'],
            route['Destination'],
        )
        return count_flights(
            all_flights,
            sort_flights_by_source_destination,
        ) == len(sort_flights_by_source_destination)


def count_flights(first_sequence, second_sequence):
    """Return the number of matches.

    Returns the number of occurrences of elements from the first sequence
    in the second sequence.

    Args:
        first_sequence (iterable): any sequence
        second_sequence (iterable): any sequence

    Returns:
        number (int): count of elements
    """
    count_elem = 0
    for elem in first_sequence:
        if elem in second_sequence:
            count_elem += 1
    return count_elem


def get_median_time(flights):
    """Return the median of the time list.

    From the list of flights, where each flight is represented by a dictionary,
    selects a time, creates a list of times and finds the median of this list.

    Args:
        flights (list): list all flights, each flight is represented
            by a dictionary.

    Returns:
        int: median of list
    """
    times = []
    for flight in flights:
        times.append(flight['TotalTravelTime'])
    sorted_times = sorted(times)

    average_index = len(sorted_times) // 2
    if len(sorted_times) % 2 == 0:
        median = (
            (sorted_times[average_index - 1] + sorted_times[average_index]) // 2
        )
    else:
        median = sorted_times[average_index]

    return median


def get_median_price(flights):
    """Return the median of the time price.

    From the list of flights, where each flight is represented by a dictionary,
    selects a price, creates a list of prices and finds the median of this list.

    Args:
        flights (list): list all flights, each flight is represented
            by a dictionary.

    Returns:
        int: median of list
    """
    prices = []
    for flight in flights:
        prices.append(flight['Price']['TicketPrice'])
    sort_prices = sorted(map(float, prices))

    average_index = len(sort_prices) // 2
    if len(sort_prices) % 2 == 0:
        median = (
            float(
                sort_prices[average_index - 1],
            ) + float(sort_prices[average_index])
        ) // 2
    else:
        median = float(sort_prices[average_index])

    return median
