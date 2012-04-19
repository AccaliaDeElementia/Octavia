#!/usr/bin/python2

from decorator import decorator
import json

from mpd import MPDClient, CommandError
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


## BEGIN: CONFIGURATION
DEBUG = True
SECRET_KEY = 'CEsufr4CrAqasp4FrUNUTHahUXAn4B+upH5tHaraFRAYaswa2RafruRaz6fAf69e'

MPD_HOST = 'localhost'
MPD_PORT = 6600
DEFAULT_PASSWORD = 'foo'

APP_NAME = 'Octavia'
APP_VERSION = '0.0.0Alpha'
APP_MAINTAINER = 'Accalia de Elementia'
APP_URL = 'https://github.com/AccaliaDeElementia/Octavia'
APP_LICENSE = 'Creative Commons Attribution 3.0 Unported'
APP_LICENSE_URL ='http://creativecommons.org/licenses/by/3.0/'
## END: CONFIGURATION

@decorator
def jsonify(func, *args, **kwargs):
    return (json.dumps(func(*args, **kwargs)),200,{'Content-Type':'application/json'})

app = Flask(__name__)
app.config.from_object (__name__)

@app.before_request
def connect():
    g.connected = False
    g.client = MPDClient()
    try:
        g.client.connect(app.config['MPD_HOST'], app.config['MPD_PORT'])
        g.connected = True
        passwd = session.get('PASSWORD', app.config['DEFAULT_PASSWORD'])
        if passwd:
            try:
                g.client.password(passwd)
            except CommandError as e:
                abort(401, e.message.split('} ',1)[1])
    except Exception as e:
        print e
        pass

@app.teardown_request
def disconnect(error):
    try:
        g.client.disconnect()
    except:
        pass

from PlayQueue import *
