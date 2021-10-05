# -*- coding: utf8 -*-
"""Definition of the fixtures of pytest."""

import pytest

from airflight.data_analysis import get_all_flights, get_all_routes


@pytest.fixture
def all_flights():
    all_flight = get_all_flights()

    def _all_flights():
        return all_flight

    return _all_flights


@pytest.fixture
def all_routes():
    all_routes = get_all_routes()

    def _all_routes():
        for route in all_routes:
            yield route

    return _all_routes
