#!/usr/bin/python
import logging
logging.disable(logging.DEBUG)

import json
import threading

from decorator import decorator

from bottle import Bottle, run, request
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

from jsonrpc2 import JsonRpcApplication
from wsgi_xmlrpc import WSGIXMLRPCApplication as XmlRpcApplication

from mpd import MPDClient

import Documentator

mpc = threading.local()

class Octavia (object):
    def __init__ (self):
        self.app = Bottle()
        self.jsonrpcapp = JsonRpcApplication()
        self.jsonrpc = self.jsonrpcapp.rpc
        self.xmlrpcapp = XmlRpcApplication()
        self.app.mount('/json', self.jsonrpcapp)
        self.app.mount('/xml', self.xmlrpcapp)
        self.app.get('/websocket', apply=[websocket], callback=self.websocket)

    def register (self, func):
        def wrapper (f, *args, **kwargs):
            try: 
                mpc.client = MPDClient()
                mpc.client.connect('127.0.0.1', 6600, 10)
                mpc.client.iterate = True
                return f(*args, **kwargs)
            finally:
                try: 
                    mpc.client.close()
                    mpc.client.disconnect()
                except: pass
        f2 = decorator(wrapper, func)
        Documentator.registerMethod(f2)
        self.jsonrpc.methods[func.__name__] = f2
        self.xmlrpcapp.dispatcher.register_function(f2)
        return func 

    def websocket(self, ws):
        while True:
            msg = ws.receive()
            if msg is not None:
                req = json.loads(msg)
                resp = self.jsonrpc(req)
                ws.send(json.dumps(resp))
            else: break

octavia = Octavia()

def filter_song(song):
    keys = ['album', 'artist', 'title', 'track', 'id', 'file', 'time', 'disc']
    return { key: song.get(key, None) for key in keys }

@octavia.register
def help(method=None):
    return Documentator.help(method)
 
import Queue
import Playlist
import Library

if __name__ == '__main__':
    run(octavia.app, host='localhost', port=8080, server=GeventWebSocketServer)
