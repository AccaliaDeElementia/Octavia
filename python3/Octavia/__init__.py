#!/usr/bin/python
import json

from bottle import Bottle, request, response, abort, run
from decorator import decorator
from mpd import MPDClient, CommandError, ConnectionError


## BEGIN: CONFIGURATION
MPD_HOST = 'localhost'
MPD_PORT = 6600
MPD_DEFAULT_PASSWORD = None

APP_NAME = 'Octavia'
APP_VERSION = '0.1.0Alpha'
APP_AUTHOR = 'Accalia de Elementia'
APP_URL = 'https://github.com/AccaliaDeElementia/Octavia'
APP_LICENSE = 'Creative Commons Attribution 3.0 Unported'
APP_LICENSE_URL = 'http://creativecommons.org/licenses/by/3.0'
##  END : CONFIGURATION

app = Bottle(__name__)

@decorator
def webMethod(func, *args, **kwargs):
    request.mpd = MPDClient()
    try:
        try:
            request.mpd.connect(MPD_HOST, MPD_PORT)
        except:
            abort (500, 'Connection to MPD failed')
        passwd = request.get_cookie('MPD_PASSWORD', MPD_DEFAULT_PASSWORD)
        if passwd:
            request.mpd.password(passwd)
        try:
            return json.dumps(func(*args, **kwargs))
        finally:
            request.mpd.disconnect()
    except CommandError as e:
        msg = e.message.split('} ',1)[1]
        code = {
            '[1':  400,
            '[2':  400,
            '[3':  401,
            '[4':  401,
            '[5':  500,
            '[50': 404,
            '[51': 413,
            '[52': 500,
            '[53': 500,
            '[54': 500,
            '[55': 400,
            '[56': 409,
        }.get(e.message.split('@',1)[0], 500)
        abort(code, msg)

@app.hook('after_request')
def allow_CORS():
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Content-Type'] = 'application/json'


