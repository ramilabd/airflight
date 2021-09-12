# from ..airflight import __version__
from airflight.data_analysis import get_all_flights, get_flights_sorted_price, get_flights_sorted_time
import operator

# def test_version():
#     assert __version__ == '0.1.0'

math_operator = {

}

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


def test_get_all_flights():
    assert len(get_all_flights()) == 200


def test_get_flights_sorted_price():
    assert checking_sorting_price(get_flights_sorted_price) == True
    assert checking_sorting_price(get_flights_sorted_price, reverse=True) == True


def test_get_flights_sorted_time():
    assert checking_sorting_time(get_flights_sorted_time) == True
    assert checking_sorting_time(get_flights_sorted_time, reverse=True) == True
