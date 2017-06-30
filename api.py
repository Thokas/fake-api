#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, run, static_file, get, post, error, request, \
    response as bottle_response, redirect
from pprint import pformat


# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        bottle_response.headers['Access-Control-Allow-Origin'] = '*'
        bottle_response.headers[
            'Access-Control-Allow-Methods'] = "GET, POST, PUT, OPTIONS"
        bottle_response.headers[
            'Access-Control-Allow-Headers'] = "Origin, Accept, Content-Type," \
                                              " X-Requested-With, X-CSRF-Token"

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

        return ''

    return _enable_cors

############################################
# Useful functions
############################################


def get_params():
    params = dict()
    for key in request.params:
        params[key] = request.params[key]

    return params


############################################
# Actual Handling
############################################

@post('/post')
@enable_cors
def all_post():
    params = get_params()

    return pformat(params)


@get('/get')
@enable_cors
def all_get():
    params = get_params()

    return pformat(params)


@get('/redirect')
@enable_cors
def redirect_to_get():
    redirect('/get')

    return ''

############################################
# HTTP Error-Handling
############################################


@error(404)
def error404(msg):
    del msg
    return 'Hier ist irgendwas schief gelaufen.\nZiel nicht gefunden :('


@error(405)
def error405(msg):
    del msg
    return 'Methode ist nicht erlaubt!'


############################################
# RUN Application
############################################
run(host='localhost', port=8080, debug=False, reloader=True)
