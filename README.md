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

# Features

- Choosing the flight direction
- The most expensive/cheapest flight
- The fastest/longest and optimal flight options

# Documentation

Доступ к ресурсам осуществляется через строку запроса методом GET протокола HTTP.

В REST API определены слудующие конечные точки:

- `/main_page` или `/`

  Главная страница веб сервиса. Здесь также написана документация.
  Тип возвращаемого ответа - `HTML`.

- `/airflights/flights/all_routes`

  Тип возвращаемого ответа - `JSON`. Содержит список маршрутов, где каждый маршрут представлен словарем, вида:

  ```python
  {
      "Destination": "BKK",
      "Source": "DXB",
      "Transfer": "DEL"    # если имеется
  },
  ```

- `/airflights/flights`

  При обращении к данной конечной точке, сервер вернет все имеющиеся авиа рейсы.
  Тип возвращаемого ответа - `JSON`. Содержит список рейсов.

- `/airflights/flights/sorted_by_direction/<source>/<destination>`

  Конечная точка принимает два параметра:

  `source` - место отправления, сокращенное наименование аэропорта. Тип параметра `string`.

  `destination` - место прибытия, сокращенное наименование аэропорта. Тип параметра `string`.

  Тип возвращаемого ответа - `JSON`, содержаший список рейсов отфильтрованных по месту отправления и прибытия.

- `/airflights/flights/sorted_by_price/<source>/<destination>`

  Конечная точка принимает два параметра:

  `source` - место отправления, сокращенное наименование аэропорта. Тип параметра `string`.

  `destination` - место прибытия, сокращенное наименование аэропорта. Тип параметра `string`.

  Тип возвращаемого ответа - `JSON`, содержаший список рейсов, отсортированных по цене.

- `/airflights/flights/sorted_by_time/<source>/<destination>`

  Конечная точка принимает два параметра:

  `source` - место отправления, сокращенное наименование аэропорта. Тип параметра `string`.

  `destination` - место прибытия, сокращенное наименование аэропорта. Тип параметра `string`.

  Тип возвращаемого ответа - `JSON`, содержаший список рейсов, отсортированных по времени перелета.

- `/airflights/flights/optimal_routes/<source>/<destination>`

  Конечная точка принимает два параметра:

  `source` - место отправления, сокращенное наименование аэропорта. Тип параметра `string`.

  `destination` - место прибытия, сокращенное наименование аэропорта. Тип параметра `string`.

  Тип возвращаемого ответа - `JSON`, содержаший список оптимальных рейсов по цене и времени перелета.

Каждый рейс в списке возвращаемом конечными точками представлен словарем, вида:

```python
{
  "Price": {
    "Currency": "...",
    "TicketPrice": "..."
  },
  "TotalTravelTime": "...",
  "flight1": {
    "ArrivalTimeStamp": "...",
    "Carrier": "...",
    "Class": "...",
    "DepartureTimeStamp": "...",
    "Destination": "...",
    "FareBasis": "...",
    "FlightNumber": "...",
    "NumberOfStops": "...",
    "Source": "...",
    "TicketType": "..."
  },
  "flight2": {
      "flight2" # по структуре повторяет "flight1", отвображается в результате поиска только если маршрут состоит из двух рейсов.
  }
},
```

# Examples

Пример запроса:
`/airflights/flights/sorted_by_direction/DXB/BKK`

ответ:

```python
[
  {
    "Price": {
      "Currency": "SGD",
      "TicketPrice": "546.80"
    },
    "TotalTravelTime": "19:30:00",
    "flight1": {
      "ArrivalTimeStamp": "2018-10-22T0445",
      "Carrier": "AirIndia",
      "Class": "G",
      "DepartureTimeStamp": "2018-10-22T0005",
      "Destination": "DEL",
      "FareBasis": "2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0",
      "FlightNumber": "996",
      "NumberOfStops": "0",
      "Source": "DXB",
      "TicketType": "E"
    },
    "flight2": {
      "ArrivalTimeStamp": "2018-10-22T1935",
      "Carrier": "AirIndia",
      "Class": "G",
      "DepartureTimeStamp": "2018-10-22T1350",
      "Destination": "BKK",
      "FareBasis": "2820231f40c802-03e6-4655-9ece-0fb1ad670b5c@@$255_DXB_DEL_996_9_00:05_$255_DEL_BKK_332_9_13:50_$255_BKK_DEL_333_9_08:50_$255_DEL_DXB_995_9_20:40__A2_0_0",
      "FlightNumber": "332",
      "NumberOfStops": "0",
      "Source": "DEL",
      "TicketType": "E"
    }
  },
  {
    "Price": {
      "Currency": "SGD",
      "TicketPrice": "623.80"
    },
    "TotalTravelTime": "18:55:00",
    "flight1": { ...
```

# Contributing

# License

# Gratitude

Реализация данного проекта была бы невозможна без знаний полученным на курсах программирования [Hexlet](https://ru.hexlet.io). Это крутейший ресурс по обучению программированию в интернете. Отличная подача информации, мозговзрывающие задания, сложные проекты и классное сообщество. Спасибо Hexlet! Я все еще продолжаю там учиться. Мои проекты:

- [python-project-lvl1](https://github.com/ramilabd/python-project-lvl1) - завершен
- [python-project-lvl2](https://github.com/ramilabd/python-project-lvl2) - в работе

Также большое спасибо сообществу [Хекслет Комьюнити](hexlet-ru.slack.com) в слаке (Slack), за ваши ответы на мои "глупые" вопросы :).

# Contacts

[Аккаунт на Hexlet](https://ru.hexlet.io/ramilabd).

[LinkedIn](https://www.linkedin.com/in/%D1%80%D0%B0%D0%BC%D0%B8%D0%BB%D1%8C-%D0%B0%D0%B1%D0%B4%D1%83%D1%80%D0%B0%D1%85%D0%BC%D0%B0%D0%BD%D0%BE%D0%B2-510793b4/)

[Аккаунт в Slack](https://hexlet-ru.slack.com/U01611HB7U3)

электропочта ramsmart@mail.ru

# Description of the test task

Данный проект является вариантом решения [тестового задания](https://github.com/KosyanMedia/test-tasks/tree/master/assisted_team) в команду ассистеда компании [Aviasales](https://www.aviasales.ru/?origin=REN)

Задание:

В папке два XML – это ответы на поисковые запросы, сделанные к одному из наших партнёров. В ответах лежат варианты перелётов (тег `Flights`) со всей необходимой информацией, чтобы отобразить билет на Aviasales.

На основе этих данных, нужно сделать вебсервис, в котором есть эндпоинты, отвечающие на следующие запросы:

- Какие варианты перелёта из DXB в BKK мы получили?
- Самый дорогой/дешёвый, быстрый/долгий и оптимальный варианты
- В чём отличия между результатами двух запросов (изменение маршрутов/условий)?

Язык реализации: `Go`
Формат ответа: `json`
По возможности использовать стандартную библиотеку.

Язык реализации: `python3`
Формат ответа: `json`
Используемые библиотеки и инструменты — всё на твой выбор.

Оценивать будем умение выполнять задачу имея неполные данные о ней, умение самостоятельно принимать решения и качество кода.
