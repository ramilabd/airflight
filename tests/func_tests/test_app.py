# -*- coding: utf8 -*-
"""Functional tests of the application."""


import jsonschema
from tests.conftest import web_service
from tests.func_tests import set_json_schemes


def test_app_airflight(web_service):
    response1 = web_service.get('/')
    response2 = web_service.get('/airflight')

    assert response1.status_code == 200
    assert response2.status_code == 200


def test_validate_response_all_flight(web_service):
    response = web_service.get('/airflight/flights')
    response_json = response.get_json()

    is_json_valide = True
    for flight in response_json:
        if flight.get('flight2') is None:
            try:
                jsonschema.validate(flight, set_json_schemes.flight1)
            except jsonschema.exceptions.ValidationError:
                is_json_valide = False
            except jsonschema.exceptions.SchemaError:
                is_json_valide = False
        else:
            try:
                jsonschema.validate(flight, set_json_schemes.flight1_flight2)
            except jsonschema.exceptions.ValidationError:
                is_json_valide = False
            except jsonschema.exceptions.SchemaError:
                is_json_valide = True

    assert is_json_valide


def test_validate_sorted_flights_by_direction(web_service):
    response = web_service.get(
        '/airflight/flights/sorted_by_direction/<source>/<destination>',
    )
    response_json = response.get_json()

    is_json_valide = True
    for flight in response_json:
        if flight.get('flight2') is None:
            try:
                jsonschema.validate(flight, set_json_schemes.flight1)
            except jsonschema.exceptions.ValidationError:
                is_json_valide = False
            except jsonschema.exceptions.SchemaError:
                is_json_valide = False
        else:
            try:
                jsonschema.validate(flight, set_json_schemes.flight1_flight2)
            except jsonschema.exceptions.ValidationError:
                is_json_valide = False
            except jsonschema.exceptions.SchemaError:
                is_json_valide = True

    assert is_json_valide
