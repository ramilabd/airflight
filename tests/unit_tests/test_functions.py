# -*- coding: utf8 -*-
"""Tests the functions of web service."""

from airflight.data_analysis import (
    get_all_flights,
    get_all_routes,
    get_flights_filtered_direction,
    get_flights_sorted_price,
    get_flights_sorted_time,
    get_optimal_route,
)


def test_get_all_flights(all_flights):
    """Test of the function get_all_flights.

    Args:
        all_flights (fixture): a fixture function that returns a function that,
            when called, returns a list of flights, where each flight is
            represented by a dictionary
    """
    assert len(all_flights()) == 200


def test_get_flights_sorted_price():
    def is_correct_sorting_by_price(reverse=False):
        flights = get_all_flights()
        sort_flights_by_price = get_flights_sorted_price(flights, reverse=reverse)
        is_correct_sort = True

        i, j = 0, 1
        while is_correct_sort and j < len(sort_flights_by_price):
            prev_price = float(sort_flights_by_price[i]['Price']['TicketPrice'])
            next_price = float(sort_flights_by_price[j]['Price']['TicketPrice'])
            if reverse:
                if prev_price < next_price:
                    is_correct_sort = False
            elif prev_price > next_price:
                    is_correct_sort = False
            i += 1
            j += 1

        return is_correct_sort

    assert is_correct_sorting_by_price() == True
    assert is_correct_sorting_by_price(reverse=True) == True


def test_get_flights_sorted_time():
    def is_correct_sorting_by_time(reverse=False):
        flights = get_all_flights()
        sort_flights_by_time = get_flights_sorted_time(flights, reverse=reverse)
        is_correct_sort = True

        i, j = 0, 1
        while is_correct_sort and j < len(sort_flights_by_time):
            prev_time = sort_flights_by_time[i]['TotalTravelTime']
            next_time = sort_flights_by_time[j]['TotalTravelTime']
            if reverse:
                if prev_time < next_time:
                    is_correct_sort = False
            elif prev_time > next_time:
                    is_correct_sort = False
            i += 1
            j += 1

        return is_correct_sort

    assert is_correct_sorting_by_time() == True
    assert is_correct_sorting_by_time(reverse=True) == True


def test_get_flights_filtered_direction():
    def is_correct_sorting_by_direction(source, destination):
        flights = get_all_flights()
        sorted_flights_with_source_destination = get_flights_filtered_direction(
                source, destination)
        sorted_flights_without_source_destination = []

        for flight in flights:
            if 'flight_2' not in flight:
                if (source != flight['flight_1']['Source'] or
                    destination != flight['flight_1']['Destination']):
                    sorted_flights_without_source_destination.append(flight)
            elif (source != flight['flight_1']['Source'] or
                    destination != flight['flight_2']['Destination']):
                    sorted_flights_without_source_destination.append(flight)

        return (len(sorted_flights_with_source_destination) +
                len(sorted_flights_without_source_destination) == len(flights))

    assert is_correct_sorting_by_direction('DXB', 'BKK') == True


def test_get_all_routes():
    all_flights = get_all_flights()
    total_count_flights = len(all_flights)
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


def test_get_optimal_route():
    all_flights = get_all_flights()
    optimal_route = get_optimal_route('DXB', 'BKK')

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

    median_time_all_flights = get_median_time(all_flights)
    median_time_optimal_route = get_median_time(optimal_route)

    median_price_all_flights = get_median_price(all_flights)
    median_price_optimal_route = get_median_price(optimal_route)

    assert median_time_optimal_route < median_time_all_flights
    assert median_price_optimal_route < median_price_all_flights
