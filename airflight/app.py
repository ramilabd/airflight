from flask import Flask, jsonify
from .data_analysis import (
    formatting_time,
    get_all_flights,
    get_flights_filtered_direction,
    get_flights_sorted_price,
    get_flights_sorted_time,
    get_all_routes,
    get_optimal_route,
    formatting_time
)


app = Flask(__name__)


@app.route('/')
@app.route('/airflight/api/v1.0')
def index():
    return 'Hello, this main page!'


@app.route('/airflight/api/v1.0/all_flights')
def receive_all_flights():
    return jsonify(formatting_time(get_all_flights()))


@app.route('/airflight/api/v1.0/sorted_flights_by_direction/<source>/<destination>')
def receive_sorted_flights_by_direction(source, destination):
    return jsonify(
        formatting_time(get_flights_filtered_direction(source, destination))
        )


@app.route('/airflight/api/v1.0/flights_sorted_price/<source>/<destination>')
def receive_flights_sorted_price(source, destination):
    return jsonify(formatting_time(get_flights_sorted_price(
        get_flights_filtered_direction(source, destination))
        ))


@app.route('/airflight/api/v1.0/flights_sorted_time/<source>/<destination>')
def receive_flight_sorted_time(source, destination):
    return jsonify(formatting_time(get_flights_sorted_time(
        get_flights_filtered_direction(source, destination))
        ))


@app.route('/airflight/api/v1.0/optimal_route/<source>/<destination>')
def receive_get_optimal_route(source, destination):
    return jsonify(formatting_time(get_optimal_route(source, destination)))


@app.route('/airflight/api/v1.0/all_routes')
def receive_get_all_route():
    return jsonify(get_all_routes())


if __name__ == '__main__':
    app.run()
