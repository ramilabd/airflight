# Airflights

[![Maintainability](https://api.codeclimate.com/v1/badges/42b4bf75465a522d573b/maintainability)](https://codeclimate.com/github/ramilabd/airflights/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/42b4bf75465a522d573b/test_coverage)](https://codeclimate.com/github/ramilabd/airflights/test_coverage)
![TestLint](https://github.com/ramilabd/airflights/actions/workflows/python-ci.yml/badge.svg)
[![Build Status](https://app.travis-ci.com/ramilabd/airflights.svg?branch=develop)](https://app.travis-ci.com/ramilabd/airflights)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![wakatime](https://wakatime.com/badge/github/ramilabd/airflights.svg)](https://wakatime.com/badge/github/ramilabd/airflights)
[![Updates](https://pyup.io/repos/github/ramilabd/airflights/shield.svg)](https://pyup.io/repos/github/ramilabd/airflights/)
[![Python 3](https://pyup.io/repos/github/ramilabd/airflights/python-3-shield.svg)](https://pyup.io/repos/github/ramilabd/airflights/)

Airflights - this is a web service for finding air tickets.

Works on [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [Flask-restful](https://flask-restful.readthedocs.io/en/latest/)

Deployed on [Heroku](https://airflights.herokuapp.com/)

# Features

- Choosing the flight direction
- The most expensive/cheapest flight
- The fastest/longest and optimal flight options

# Examples

A simple example request:

```
  https://airflights.herokuapp.com/all_flights
```

Returns the response:

```json
[{"flight1": {"Carrier": "AirIndia", "FlightNumber": "996", "Source": "DXB", "Destination": "DEL", "DepartureTimeStamp": "2018-10-22T0005", "ArrivalTimeStamp": "2018-10-22T0445", "Class": "G", "NumberOfStops": "0", "FareBasis": "2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_D .......]
```

Request with parameters:

```
  https://airflights.herokuapp.com/all_flights/optimal_routes/DXB/BKK
```

Returns the response:

```json
[{"flight1": {"Carrier": "JetAirways", "FlightNumber": "537", "Source": "DXB", "Destination": "BOM", "DepartureTimeStamp": "2018-10-22T1845", "ArrivalTimeStamp": "2018-10-22T2330", "Class": "V", "NumberOfStops": "0", "FareBasis": "2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_BOM_537_6_18:45_$255_BOM_BKK_62_6_01:05_$255_BKK_BOM_61_6_08:55_$255_BOM_DXB_538_6_15:40__A2_0_0", "TicketType": "E"}, "Price": {"TicketPrice": "647.40", .... ]
```

# Documentation

## Request methods

Only the GET HTTP method is used.

## Response

Returns a response in JSON format. If there is no data, returns an empty JSON and status code 404.

## Endpoints:

All our API’s are prefixed with `https://airflights.herokuapp.com`.

```
  /docs
```

or

```
  /
```

Return: web service documentation page.

```
  /all_flights
```

Return JSON: all possible flights. Example of flights representation:

```json
{
  "flight1": {
    "Carrier": "AirIndia",
    "FlightNumber": "996",
    "Source": "DXB",
    "Destination": "DEL",
    "DepartureTimeStamp": "2018-10-22T0005",
    "ArrivalTimeStamp": "2018-10-22T0445",
    "Class": "G",
    "NumberOfStops": "0",
    "FareBasis": "2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0",
    "TicketType": "E"
  },
  "Price": {
    "TicketPrice": "546.80",
    "Currency": "SGD"
  },
  "flight2": {
    "Carrier": "AirIndia",
    "FlightNumber": "332",
    "Source": "DEL",
    "Destination": "BKK",
    "DepartureTimeStamp": "2018-10-22T1350",
    "ArrivalTimeStamp": "2018-10-22T1935",
    "Class": "G",
    "NumberOfStops": "0",
    "FareBasis": "2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0",
    "TicketType": "E"
  },
  "TotalTravelTime": "19:30:00"
}
```

```
  /all_routes
```

Return JSON: all possible flight routes. Example of route representation:

```json
{
  "Source": "DXB",
  "Transfer": "DEL",
  "Destination": "BKK"
}
```

Filters flights by destinations:

```
  /all_flights/sorted_by_direction/<source>/<destination>
```

Sorts flights by price:

```
  /all_flights/sorted_by_price/<source>/<destination>
```

Sorts flights by travel time:

```
  /all_flights/sorted_by_time/<source>/<destination>
```

Returns optimal routes by price and travel time:

```
  /all_flights/optimal_routes/<source>/<destination>
```

`<source>` - departure airport, IATA Airport Code is a three-letter unique identifier. Three uppercase Latin characters.

`<destination>` - arrival airport, IATA Airport Code is a three-letter unique identifier. Three uppercase Latin characters.

# Description of the test task

This project is a variant of the solution of the [test task](https://github.com/KosyanMedia/test-tasks/tree/master/assisted_team) to the company's assistant team [Aviasales](https://www.aviasales.ru/?origin=REN)

# Contacts

[Account in Hexlet](https://ru.hexlet.io/ramilabd).

[LinkedIn](https://www.linkedin.com/in/%D1%80%D0%B0%D0%BC%D0%B8%D0%BB%D1%8C-%D0%B0%D0%B1%D0%B4%D1%83%D1%80%D0%B0%D1%85%D0%BC%D0%B0%D0%BD%D0%BE%D0%B2-510793b4/)

[Account in Slack](https://hexlet-ru.slack.com/U01611HB7U3)

email: rramil.abd@gmail.com

# Gratitude

This project was implemented thanks to the knowledge gained in programming courses [Hexlet](https://ru.hexlet.io). This is a cool resource for learning programming on the Internet. Excellent presentation of information, brain-blowing tasks, complex projects and a cool community. Thanks Hexlet! I'm still studying there. My Projects:

- [python-project-lvl1](https://github.com/ramilabd/python-project-lvl1) - completed
- [python-project-lvl2](https://github.com/ramilabd/python-project-lvl2) - at work

Also many thanks to the community [Хекслет Комьюнити](hexlet-ru.slack.com) in Slack, for your answers to my stupid questions :)

# License

Copyright Ramil Abdurakhmanov, 2021.

Distributed under the terms of the MIT license, pytest is free and open source software.
