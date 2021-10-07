# -*- coding: utf8 -*-
"""Definition of the fixtures of pytest."""

import pytest
from airflight.data_analysis import get_all_flights, get_all_routes


def get_function(func):
    """Return of function.

    Decorator.
    Wraps the accepted function in a wrapper and returns the wrapper.

    Args:
        func (function): wrapped function.

    Returns:
        func (function): wrapper with function.
    """
    def wrapper():
        return func

    return wrapper


@pytest.fixture(scope='module', autouse=True)
def all_flights():
    """Return list of flights.

        Fixture function.

    Returns:
        list: list: list of flights, each flight
            is represented by a dictionary.
    """
    return get_all_flights()


@pytest.fixture(scope='module', autouse=True)
@get_function
def get_routes_in_parts():
    """Return all possible routes.

        Fixture function.
        Returns each route from the list separately.
        Each route is represented by a dictionary, in which the following
        are specified source, transfer and destination

    Yields:
        dict: dictionary of the form
            {'Source': ..., 'Transfer': ..., 'Destination': ...}
    """
    yield from get_all_routes()
