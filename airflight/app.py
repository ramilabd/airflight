# -*- coding:utf-8 -*-
"""Flask application module."""


from data_analysis import (
    formatting_time,
    get_all_flights,
    get_all_routes,
    get_flights_filtered_direction,
    get_flights_sorted_price,
    get_flights_sorted_time,
    get_optimal_route,
)
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
@app.route('/airflight')
def index():
    """Route handler '/' or 'airflight'.

    Returns:
        html: main page of web service.
    """
    return 'Hello, this main page!'


@app.route('/airflight/flights')
def receive_all_flights():
    """Route handler '/flights'.

    Calls the funcrion 'get_all_flights',
    formats her response in 'json', puts the time (datetime) in the string.

    Returns:
        json: list of flights.
    """
    return jsonify(formatting_time(get_all_flights()))


@app.route('/airflight/flights/sorted_by_direction/<source>/<destination>')
def receive_sorted_flights_by_direction(source, destination):
    """Route handler '/sorted_by_direction'.

    Calls the funcrion 'get_flights_filtered_direction',
    formats her response in 'json', puts the time (datetime) in the string.

    Args:
        source (str): name of the departure airport.
        destination (str): name of the arrival airport.

    Returns:
        json: list of flights.
    """
    return jsonify(
        formatting_time(get_flights_filtered_direction(
            source,
            destination,
        )))


@app.route('/airflight/flights/sorted_by_price/<source>/<destination>')
def receive_flights_sorted_price(source, destination):
    """Route handler '/sorted_by_price'.

    Calls the funcrion 'get_flights_sorted_price', formats her response in
    'json', puts the time (datetime) in the string. Parameters "source" and
    "destination" passed to the function "get_flights_filtered_direction".

    Args:
        source (str): name of the departure airport.
        destination (str): name of the arrival airport.

    Returns:
        json: list of flights.
    """
    return jsonify(formatting_time(get_flights_sorted_price(
        get_flights_filtered_direction(
            source,
            destination,
        ))))


@app.route('/airflight/flights/sorted_by_time/<source>/<destination>')
def receive_flight_sorted_time(source, destination):
    """Route handler '/sorted_by_time'.

    Calls the funcrion 'get_flights_sorted_time', formats her response in
    'json', puts the time (datetime) in the string. Parameters "source" and
    "destination" passed to the function "get_flights_filtered_direction".

    Args:
        source (str): name of the departure airport.
        destination (str): name of the arrival airport.

    Returns:
        json: list of flights.
    """
    return jsonify(formatting_time(get_flights_sorted_time(
        get_flights_filtered_direction(
            source,
            destination,
        ))))


@app.route('/airflight/flights/optimal_routes/<source>/<destination>')
def receive_get_optimal_route(source, destination):
    """Route handler '/optimal_routes'.

    Calls the funcrion 'get_optimal_route', formats her response in 'json',
    puts the time (datetime) in the string.

    Args:
        source (str): name of the departure airport.
        destination (str): name of the arrival airport.

    Returns:
        json: list of flights.
    """
    return jsonify(formatting_time(get_optimal_route(source, destination)))


@app.route('/airflight/flights/routes')
def receive_get_all_route():
    """Route handler '/routes'.

    Calls the funcrion 'get_all_routes', formats her response in 'json',
    puts the time (datetime) in the string.

    Returns:
        json: list of routes.
    """
    return jsonify(get_all_routes())


if __name__ == '__main__':
    app.run()
