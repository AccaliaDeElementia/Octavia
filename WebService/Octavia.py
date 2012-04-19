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


@app.route('/')
@jsonify
def index():
    mpd_status = g.client.status() if g.connected else {}
    return {
        'application': {
            'name': app.config['APP_NAME'],
            'version': app.config['APP_VERSION'],
            'url': app.config['APP_URL'],
            'license': app.config['APP_LICENSE'],
            'license_url': app.config['APP_LICENSE_URL'],
        },
        'client' : {
            'host': app.config['MPD_HOST'],
            'port': app.config['MPD_PORT'],
            'password': session.get('PASSWORD', app.config['DEFAULT_PASSWORD']),
            'version': g.client.mpd_version,
            'state': mpd_status.get('state', '')
        }
    }

def __filter_song(song):
    for attr in song.keys():
        if not attr in ['album', 'artist', 'title', 'track', 'id', 'file']:
            del song[attr]
    return song
 

@app.route('/playlist/')
@app.route('/playlist/list')
@jsonify
def list_playlist():
    playlist = g.client.playlistinfo()
    return [__filter_song(song) for song in playlist]

@app.route('/playlist/current')
@jsonify
def show_current():
    return g.client.currentsong()

@app.route('/playlist/save', methods=['POST'])
@jsonify
def save_paylist():
    data = request.json
    if 'name' not in data.keys():
        abort(400, "name not specified")
    try: 
        g.client.save(data['name'])
    except CommandError as e:
        abort(409, e.message.split('} ',1)[1])
    return True

@app.route('/playlists/')
@jsonify
def list_playlists():
    data = g.client.listplaylists()
    return [playlist['playlist'] for playlist in data]

@app.route('/playlists/<name>')
@jsonify
def show_playlist(name):
    data = g.client.listplaylistinfo(name)
    return [__filter_song(song) for song in data]

@app.route('/playlists/<name>', methods=['DELETE'])
@jsonify
def delete_paylist(name):
    try: 
        g.client.rm(name)
    except CommandError as e:
        abort(409, e.message.split('} ',1)[1])
    return True


if __name__ == '__main__':
    app.run()
