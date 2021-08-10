#!/home/wanderer/.pyenv/versions/3.8.5/bin/python
from flask import Flask, jsonify
from .data_analysis import get_all_flights, get_flights_sorted_price


app = Flask(__name__)


@app.route('/')
@app.route('/airflight/api/v1.0')
def index():
    return 'Hello, this main page!'


@app.route('/airflight/api/v1.0/all_flights')
def receive_all_flights():
    return jsonify(get_all_flights())


@app.route('/airflight/api/v1.0/flights_sorted_price/<compare>')
def receive_flights_sorted_price(compare):
    return jsonify(get_flights_sorted_price(compare))


if __name__ == '__main__':
    app.run(debug=True)
