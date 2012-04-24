#!/usr/bin/python2
import Octavia
app= Octavia.app

from datetime import datetime

from flask import request, session, g

def status():
    nan = float('nan')
    status = g.client.status()
    return {
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
    }
@app.route('/playback')
@Octavia.WebMethod
def get_status():
    return status()

@app.route('/playback', methods=['POST'])
@Octavia.WebMethod
def set_status():
    before = g.client.status()
    data = Octavia.get_data()
    keys = data.keys()
    g.client.command_list_ok_begin()
    if 'playback' in keys:
        value = data['playback']
        {
            'play': g.client.play,
            'pause': g.client.pause,
            'stop': g.client.pause,
            'toggle': lambda: g.client.play() if before.get('state', 'play') != 'play' else g.client.pause()
        }.get(value, lambda: None)()
    for func in ['repeat', 'consume', 'random', 'single']:
        if func in keys:
            getattr(g.client, func)('1' if data[func] else '0')
    if 'mixramp' in keys:
        ikeys = data['mixramp'].keys()
        for func in ['db', 'delay']:
            if fun in ikeys:
                getattr(g.client, 'mixramp'+func)(data['mixramp'][func])
    if 'volume' in keys:
        g.client.setvol(data['volume'])
    if 'crossfade' in keys:
        g.client.crossfade(data['crossfade'])
    g.client.command_list_end()
    return status()
