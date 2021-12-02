# -*- coding:utf-8 -*-
"""Flask application module."""

from itertools import chain

from airflights.auxiliary_func import formatting_time
from airflights.data_analysis import (
    get_all_flights,
    get_all_routes,
    get_flights_filtered_direction,
    get_flights_sorted_price,
    get_flights_sorted_time,
    get_optimal_route,
)
from flask import Flask, abort
from flask_restful import Api, Resource

app = Flask(__name__.split('.')[0])
api = Api(app, default_mediatype='application/json')


def is_valid_parameters(source, destination):
    print('is_valid_..:', source, ': ', type(source))

    all_routes = get_all_routes()
    routes = (list(route.values()) for route in all_routes)
    airports = set(chain(*routes))

    if source in airports and destination in airports:
        return True
    return False


class Docs(Resource):
    """Represents a specific RESTful resource.

        Provides a 'get()' method for the HTTP GET method.
        RESTful resource: '/docs' or '/'.

    Args:
        Resource (class flask_restful.Resource):
            https://flask-restful.readthedocs.io/en/latest/api.html
    """

    def get(self):
        """Request a resource represented by a class.

        Returns:
            string: main page of web service.
        """
        return 'Hello, this main page!', 200


class Flights(Resource):
    """Represents a specific RESTful resource.

        Provides a 'get()' method for the HTTP GET method.
        RESTful resource: '/all_flights'.

    Args:
        Resource (class flask_restful.Resource):
            https://flask-restful.readthedocs.io/en/latest/api.html
    """

    def get(self):
        """Request a resource represented by a class.

            Call the function 'get_all_flights'.
            In the received response, the 'formatting_time' function changes
            the time representation from datetime to a string.

        Returns:
            list: list of all flights.
        """
        return formatting_time(get_all_flights()), 200

class Routes(Resource):
    """Represents a specific RESTful resource.

        Provides a 'get()' method for the HTTP GET method.
        RESTful resource: '/all_routes'.

    Args:
        Resource (class flask_restful.Resource):
            https://flask-restful.readthedocs.io/en/latest/api.html
    """

    def get(self):
        """Request a resource represented by a class.

            Call the function 'get_all_routes'.

        Returns:
            list: list of routes, each route is represented by a dictionary
            of the form {'Source': ..., 'Transfer': ..., 'Destination': ...}.
        """
        return get_all_routes(), 200


class Direction(Resource):
    """Represents a specific RESTful resource.

        Provides a 'get()' method for the HTTP GET method.
        RESTful resource:
        '/all_flights/sorted_by_direction/<source>/<destination>'

    Args:
        Resource (class flask_restful.Resource):
            https://flask-restful.readthedocs.io/en/latest/api.html
    """

    def get(self, source, destination):
        """Request a resource represented by a class.

            Calls the 'get_flights_filtered_direction' function.
            In the received response, the 'formatting_time' function changes
            the time representation from datetime to a string.
            Parameters "source" and "destination" passed to the
            function "get_flights_filtered_direction".

        Args:
            source (str): name of the departure airport.
            destination (str): name of the arrival airport.

        Returns:
            list: list of flights.
        """
        if is_valid_parameters(source, destination):
            return formatting_time(get_flights_filtered_direction(
                source,
                destination,
            )), 200
        return []

class SortedPrice(Resource):
    """Represents a specific RESTful resource.

        Provides a 'get()' method for the HTTP GET method.
        RESTful resource:
        '/all_flights/sorted_by_price/<source>/<destination>'.

    Args:
        Resource (class flask_restful.Resource):
            https://flask-restful.readthedocs.io/en/latest/api.html
    """

    def get(self, source, destination):
        """Request a resource represented by a class.

            Calls the 'get_flights_sorted_price' function.
            In the received response, the 'formatting_time' function changes
            the time representation from datetime to a string.
            Parameters "source" and "destination" passed to the
            function "get_flights_filtered_direction".

        Args:
            source (str): name of the departure airport.
            destination (str): name of the arrival airport.

        Returns:
            list: list of flights.
        """
        return formatting_time(get_flights_sorted_price(
            get_flights_filtered_direction(
                source,
                destination,
            )))


class SortedTime(Resource):
    """Represents a specific RESTful resource.

        Provides a 'get()' method for the HTTP GET method.
        RESTful resource:
        '/all_flights/sorted_by_time/<source>/<destination>'.

    Args:
        Resource (class flask_restful.Resource):
            https://flask-restful.readthedocs.io/en/latest/api.html
    """

    def get(self, source, destination):
        """Request a resource represented by a class.

            Calls the 'get_flights_sorted_time' function.
            In the received response, the 'formatting_time' function changes
            the time representation from datetime to a string.
            Parameters "source" and "destination" passed to the
            function "get_flights_filtered_direction".

        Args:
            source (str): name of the departure airport.
            destination (str): name of the arrival airport.

        Returns:
            list: list of flights.
        """
        return formatting_time(get_flights_sorted_time(
            get_flights_filtered_direction(
                source,
                destination,
            )))


class OptimalRoutes(Resource):
    """Represents a specific RESTful resource.

        Provides a 'get()' method for the HTTP GET method.
        RESTful resource:
        '/all_flights/optimal_routes/<source>/<destination>'.

    Args:
        Resource (class flask_restful.Resource):
            https://flask-restful.readthedocs.io/en/latest/api.html
    """

    def get(self, source, destination):
        """Request a resource represented by a class.

            Calls the 'get_optimal_route' function.
            In the received response, the 'formatting_time' function changes
            the time representation from datetime to a string.
            Parameters "source" and "destination" passed to the
            function 'get_optimal_route'.

        Args:
            source (str): name of the departure airport.
            destination (str): name of the arrival airport.

        Returns:
            list: list of optimal flights.
        """
        return formatting_time(get_optimal_route(source, destination))


api.add_resource(Docs, '/', '/docs', endpoint='docs')
api.add_resource(Flights, '/all_flights', endpoint='flights')
api.add_resource(Routes, '/all_routes', endpoint='routes')
api.add_resource(
    Direction,
    '/all_flights/sorted_by_direction/<source>/<destination>',
    endpoint='direction',
)
api.add_resource(
    SortedPrice,
    '/all_flights/sorted_by_price/<source>/<destination>',
    endpoint='sortedprice',
)
api.add_resource(
    SortedTime,
    '/all_flights/sorted_by_time/<source>/<destination>',
    endpoint='sortedtime',
)
api.add_resource(
    OptimalRoutes,
    '/all_flights/optimal_routes/<source>/<destination>',
    endpoint='optimalroutes',
)


if __name__ == '__main__':
    app.run()
