# -*- coding:utf-8 -*-
"""Module handler of errors."""


from app import app
from flask import render_template


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error404.html'), 404


@app.errorhandler(400)
def bad_request_error(error):
    return render_template('error400.html'), 400


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error404.html'), 404


@app.errorhandler(400)
def bad_request_error(error):
    return render_template('error400.html'), 400
