# -*- coding:utf-8 -*-
"""Tests."""

from airflight.data_analysis import (
    get_all_routes,
    get_flights_filtered_direction,
    get_flights_sorted_price,
    get_flights_sorted_time,
    get_optimal_route,
)


def test_get_all_flights(all_flights):
    """Test of the function get_all_flights.

    Args:
        all_flights (fixture): function-fixture (data factory) returns
            function that return list of flights, each flight is
            represented by a dictionary.
    """
    assert len(all_flights()) == 200


def test_get_flights_sorted_price(all_flights):
    """Test of the function get_flights_sorted_price.

    Args:
        all_flights (fixture): function-fixture (data factory) returns
            function that return list of flights, each flight is
            represented by a dictionary.
    """
    for param_sort in (False, True):
        sort_flights_by_price = get_flights_sorted_price(
            all_flights(),
            reverse=param_sort,
        )
        is_correct_sort = True

        index = 0
        while is_correct_sort and index + 1 < len(sort_flights_by_price):
            prev_price = float(
                sort_flights_by_price[index]['Price']['TicketPrice'],
            )
            next_price = float(
                sort_flights_by_price[index + 1]['Price']['TicketPrice'],
            )
            if param_sort:
                if prev_price < next_price:
                    is_correct_sort = False
            elif prev_price > next_price:
                is_correct_sort = False
            index += 1

    assert is_correct_sort == True


def test_get_flights_sorted_time(all_flights):
    """Test of the function get_flights_sorted_time.

    Args:
        all_flights (fixture): function-fixture (data factory) returns
            function that return list of flights, each flight is
            represented by a dictionary.
    """
    results_is_correct_sort = []
    for param_sort in (False, True):
        sort_flights_by_time = get_flights_sorted_time(
            all_flights(),
            reverse=param_sort,
        )
        is_correct_sort = True

        prev_index, next_index = 0, 1
        while is_correct_sort and next_index < len(sort_flights_by_time):
            prev_time = sort_flights_by_time[prev_index]['TotalTravelTime']
            next_time = sort_flights_by_time[next_index]['TotalTravelTime']
            if param_sort:
                if prev_time < next_time:
                    is_correct_sort = False
            elif prev_time > next_time:
                is_correct_sort = False
            prev_index += 1
            next_index += 1

        results_is_correct_sort.append(is_correct_sort)

    assert all(results_is_correct_sort) == True


def test_get_flights_filtered_direction(all_flights, parameters_for_filtered_direction):
    """Test of the function get_flights_filtered_direction.

    Args:
        all_flights (fixture): function-fixture (data factory) returns
            function that return list of flights, each flight is
            represented by a dictionary.
        parameters_for_filtered_direction (fixture): function-fixture
            (data factory) returns list of routes (source, transfer,
            destination), each route is represented by a dictionary.
    """
    for route in parameters_for_filtered_direction:
        sorted_flights_with_source_destination = get_flights_filtered_direction(
            source=route['Source'],
            destination=route['Destination'])

        sorted_flights_without_source_destination = []
        flights = all_flights()

        for flight in flights:
            if 'flight_2' not in flight:
                if (route['Source'] != flight['flight_1']['Source'] or
                    route['Destination'] != flight['flight_1']['Destination']):
                    sorted_flights_without_source_destination.append(flight)
            elif (route['Source'] != flight['flight_1']['Source'] or
                    route['Destination'] != flight['flight_2']['Destination']):
                    sorted_flights_without_source_destination.append(flight)

        assert (len(sorted_flights_with_source_destination) +
                len(sorted_flights_without_source_destination) == len(flights))


def get_median_time(flights):
    times = []

    for flight in flights:
        times.append(flight['TotalTravelTime'])
    sorted_times = sorted(times)
    if len(sorted_times) % 2 == 0:
        median = (sorted_times[(len(sorted_times) // 2) - 1] + sorted_times[len(sorted_times) // 2]) // 2
    else:
        median = sorted_times[len(sorted_times) // 2]

    return median


def get_median_price(flights):
    prices = []

    for flight in flights:
        prices.append(flight['Price']['TicketPrice'])
    sorted_prices = sorted(list(map(float, prices)))
    if len(sorted_prices) % 2 == 0:
        median = (float(sorted_prices[(len(sorted_prices) // 2) - 1]) + float(sorted_prices[len(sorted_prices) // 2])) // 2
    else:
        median = float(sorted_prices[len(sorted_prices) // 2])

    return median


def test_get_all_routes(all_flights):
    """Test of the function get_all_routes."""
    total_count_flights = len(all_flights())
    all_routes = get_all_routes()
    count_each_route = {}
    for route in all_routes:
        direction = '{0}-{1}-{2}'.format(route['Source'],
                                        route.get('Transfer', None),
                                        route['Destination'])
        if direction in count_each_route:
            count_each_route[direction] += 1
        else:
            count_each_route[direction] = 1

    assert sum(count_each_route.values()) == total_count_flights


def test_get_optimal_route(all_flights):
    """Test of the function get_optimal_route.

    Args:
        all_flights (fixture): function-fixture (data factory) returns
            function that return list of flights, each flight is
            represented by a dictionary.
    """
    optimal_route = get_optimal_route('DXB', 'BKK')

    median_time_all_flights = get_median_time(all_flights())
    median_time_optimal_route = get_median_time(optimal_route)

    median_price_all_flights = get_median_price(all_flights())
    median_price_optimal_route = get_median_price(optimal_route)

    assert median_time_optimal_route < median_time_all_flights
    assert median_price_optimal_route < median_price_all_flights
