# -*- coding: utf8 -*-
"""Definition of the fixtures of pytest."""

import pytest

from airflight.data_analysis import get_all_flights


@pytest.fixture
def all_flights():
    all_flight = get_all_flights()

    def _all_flights():
        return all_flight

    return _all_flights
