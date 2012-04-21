#!/usr/bin/python2
import Octavia
app= Octavia.app

from datetime import datetime

from mpd import MPDClient, CommandError
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

@app.route('/')
@app.route('/about')
@Octavia.WebMethod
def index():
    mpd_status = g.client.status()
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

@app.route('/status')
@Octavia.WebMethod
def status():
    nan = float('nan')
    status = g.client.status()
    stats = g.client.stats()
    return {
        'playlist': {
            'length': int(status.get('playlistlength', -1)),
            'current': {
                'id': int(status.get('songid', -1)),
                'time': status.get('time', ''),
                'elapsed': status.get('elapsed', ''),
            },
            'next': {
                'id': int(status.get('nextid', -1)),
            }
        },
        'state': {
            'playback': status.get('state', 'unknown'),
            'bitrate': int(status.get('bitrate', 0)),
            'audio': status.get('audio'),
            'volume': float(status.get('volume', nan)),
            'repeat': True if status.get('repeat', '0') == '1' else False,
            'consume': True if status.get('consume', '0') == '1' else False,
            'random': True if status.get('random', '0') == '1' else False,
            'single': True if status.get('single', '0') == '1' else False,
            'crossfade': float(status.get('xfade', 0)),
            'mixramp': {
                'db': float(status.get('mixrampdb',0)),
                'delay': float(status.get('mixrampdelay', 0)),
            }

        },
        'database': {
            'artists': int(stats.get('artists', -1)),
            'albums': int(stats.get('albums', -1)),
            'songs': int(stats.get('songs', -1)),
            'uptime': int(stats.get('uptime', -1)),
            'playtime': int(stats.get('playtime', -1)),
            'last_update': int(stats.get('db_update')),
            'total_playtime': int(stats.get('db_playtime'))
        }
    }


