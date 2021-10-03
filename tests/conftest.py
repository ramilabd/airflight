# -*- coding:utf-8 -*-
"""Fixtures for tests are defined."""

import pytest

from airflight.data_analysis import get_all_flights, get_all_routes


@pytest.fixture
def all_flights():
    """Fixture that returns list all flights"""
    all_flights = get_all_flights()

    def _all_flights():
        return all_flights

    return _all_flights

@pytest.fixture
def parameters_for_filtered_direction():
    return get_all_routes()
