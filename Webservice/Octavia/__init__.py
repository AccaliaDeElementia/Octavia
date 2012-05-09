#!/usr/bin/python2

from decorator import decorator
import json
import re

from mpd import MPDClient, CommandError, ConnectionError
from flask import Flask, request, session, g, abort


## BEGIN: CONFIGURATION
DEBUG = True
SECRET_KEY = 'CEsufr4CrAqasp4FrUNUTHahUXAn4B+upH5tHaraFRAYaswa2RafruRaz6fAf69e'

MPD_HOST = 'localhost'
MPD_PORT = 6600
DEFAULT_PASSWORD = None

APP_NAME = 'Octavia'
APP_VERSION = '0.0.0Alpha'
APP_MAINTAINER = 'Accalia de Elementia'
APP_URL = 'https://github.com/AccaliaDeElementia/Octavia'
APP_LICENSE = 'Creative Commons Attribution 3.0 Unported'
APP_LICENSE_URL ='http://creativecommons.org/licenses/by/3.0/'
## END: CONFIGURATION

@decorator
def WebMethod (func, *args, **kwargs):
    g.client = MPDClient()
    try:
        try:
            g.client.connect(app.config['MPD_HOST'], app.config['MPD_PORT'])
        except:
            abort(500, 'Connection to MPD failed')
        passwd = session.get('PASSWORD', app.config['DEFAULT_PASSWORD'])
        if passwd:
            g.client.password(passwd)
        try:
            result = func(*args, **kwargs)
            return json.dumps((result),200,{'Content-Type':'application/json'})
        finally:
            g.client.disconnect()
    except CommandError as e:
        msg = e.message.split('} ', 1)[1]
        mpd_code = e.message.split('@',1)[0]
        code = {
            '[1': 400,
            '[2': 400,
            '[3': 401,
            '[4': 401,
            '[5': 500,
            '[50': 404,
            '[51': 413,
            '[52': 500,
            '[53': 500,
            '[54': 500,
            '[55': 400,
            '[56': 409
        }.get(mpd_code, 500)
        abort(code, msg)
    except ConnectionError:
        pass
    except Exception as e:
        if not app.config['DEBUG']:
            abort(500, e.message)
        else:
            raise e
        
def get_data():
    data = request.json
    if not data:
        data = json.loads(request.form.keys()[0])
    return data

def get_list_songs(allow_id = True, needed_keys=None):
    error = lambda: abort(400, 'input must be a list of song objects')
    attr_error = lambda: abort(400, 'song objects for tbhis method must have'+
                          ' additional attributes: %s' % ' '.join(needed_keys))
    is_song = lambda keys: 'file' in keys
    if allow_id:
        is_song = lambda keys: 'id' in keys or 'file' in keys
    data = get_data()
    if type(data) != list:
        error()
    for song in data:
        if type(song) != dict:
            error()
        keys = song.keys()
        if not is_song(keys):
            error()
        if needed_keys:
            for nkey in needed_keys:
                if nkey not in keys:
                    attr_error()
    return data

def sort_list(items, get_key):
    tokenize = re.compile(r'(\d+)|(\D+)').findall
    def sort_key(item):
        return tuple( int(num) if num else alpha for num, alpha in tokenize(get_key(item)))
    return list(sorted(items, key=sort_key))

def filter_song(song):
    fsong = {
        'album': '',
        'artist': '',
        'title': '', 
        'track': '', 
        'id': -1, 
        'file': '', 
        'time': -1
    }
    keys = fsong.keys()
    for attr in song.keys():
        if attr in keys:
            if type(fsong[attr]) == int:
                fsong[attr] = int(song[attr])
            else:
                fsong[attr] = song[attr]
    return fsong

def filter_matches(needles, haystack, formatter): 
    results = []
    matches = lambda a, b: (str(a['id']) == b['id'] if 'id' in a.keys()
                            else a['file'] == b['file'])
    for needle in needles:
        results += [formatter(needle, straw) for straw in haystack if
                    matches(needle, straw)]
    if len(results) < 1:
        abort(404, 'No songs matching criteria found')
    return results 
 
app = Flask(__name__)
app.config.from_object (__name__)

@app.after_request
def CORS_adjust(resp):
    # Allow Cross Site Scripting requests using JavaScript
    # TODO: only allow methods that the endpoint is willing to accept anyway.
    resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET, POST, PUT, DELETE'
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Content-Type'] = 'application/json'
    return resp

import Octavia.Playback
import Octavia.Library
import Octavia.Queue
import Octavia.Status
import Octavia.Playlist
