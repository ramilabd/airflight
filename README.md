# Решение [тестового задания](https://github.com/KosyanMedia/test-tasks/tree/master/assisted_team) в команду ассистеда компании [Aviasales](https://www.aviasales.ru/?origin=REN)

[![Maintainability](https://api.codeclimate.com/v1/badges/b3bfee84eada6b695083/maintainability)](https://codeclimate.com/github/ramilabd/airflight/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b3bfee84eada6b695083/test_coverage)](https://codeclimate.com/github/ramilabd/airflight/test_coverage)
![TestLint](https://github.com/ramilabd/airflight/actions/workflows/python-ci.yml/badge.svg)
[![Build Status](https://app.travis-ci.com/ramilabd/aviasales-assisted_team_solution.svg?branch=main)](https://app.travis-ci.com/ramilabd/airflight)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![wakatime](https://wakatime.com/badge/user/1385d92c-8dfb-4f90-aece-78701e17aaa6/project/47fa1668-7cd4-4e72-9680-11f5099cb2f6.svg)](https://wakatime.com/badge/user/1385d92c-8dfb-4f90-aece-78701e17aaa6/project/47fa1668-7cd4-4e72-9680-11f5099cb2f6)
[![Updates](https://pyup.io/repos/github/ramilabd/airflight/shield.svg)](https://pyup.io/repos/github/ramilabd/airflight/)
[![Python 3](https://pyup.io/repos/github/ramilabd/airflight/python-3-shield.svg)](https://pyup.io/repos/github/ramilabd/airflight/)

## Описание

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
