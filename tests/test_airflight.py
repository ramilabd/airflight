# from ..airflight import __version__
from airflight.data_analysis import get_all_flights, get_flights_sorted_price, get_flights_sorted_time, get_flights_sorted_direction
import operator

# def test_version():
#     assert __version__ == '0.1.0'


def test_get_all_flights():
    assert len(get_all_flights()) == 200


def test_get_flights_sorted_price():
    def checking_sorting_price(func, reverse=False):
        sort_flights = func(get_all_flights(), reverse=reverse)
        sort_correct = True

        i, j = 0, 1
        while sort_correct and j < len(sort_flights):
            prev_price = float(sort_flights[i]['Price']['TicketPrice'])
            next_price = float(sort_flights[j]['Price']['TicketPrice'])
            if reverse:
                if prev_price < next_price:
                    sort_correct = False
            elif prev_price > next_price:
                    sort_correct = False
            i += 1
            j += 1

        return sort_correct

    assert checking_sorting_price(get_flights_sorted_price) == True
    assert checking_sorting_price(get_flights_sorted_price, reverse=True) == True
    assert checking_sorting_price(get_flights_sorted_price, reverse=True) == True


def test_get_flights_sorted_time():
    def checking_sorting_time(func, reverse=False):
            sort_flights = func(get_all_flights(), reverse=reverse)
            sort_correct = True

            i, j = 0, 1
            while sort_correct and j < len(sort_flights):
                prev_time = sort_flights[i]['TotalTravelTime']
                next_time = sort_flights[j]['TotalTravelTime']
                if reverse:
                    if prev_time < next_time:
                        sort_correct = False
                elif prev_time > next_time:
                        sort_correct = False
                i += 1
                j += 1

            return sort_correct

    assert checking_sorting_time(get_flights_sorted_time) == True
    assert checking_sorting_time(get_flights_sorted_time, reverse=True) == True


def test_get_flights_sorted_direction():
    def checking_sorted_direction(func, source, destination):
        all_flights = get_all_flights()

        sorted_flights_with_source_destination = func(source, destination)
        sorted_flights_without_source_destination = []

        for flight in all_flights:
            if 'flight_2' not in flight:
                if source != flight['flight_1']['Source'] or destination != flight['flight_1']['Destination']:
                    sorted_flights_without_source_destination.append(flight)
            elif source != flight['flight_1']['Source'] or destination != flight['flight_2']['Destination']:
                    sorted_flights_without_source_destination.append(flight)

        return len(sorted_flights_with_source_destination) + len(sorted_flights_without_source_destination) == len(all_flights)

    assert checking_sorted_direction(get_flights_sorted_direction, 'DXB', 'BKK') == True
