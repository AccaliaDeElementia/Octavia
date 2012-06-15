#!/usr/bin/python
import json

from decorator import decorator

from bottle import Bottle, run, request
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

from jsonrpc2 import JsonRpcApplication
from wsgi_xmlrpc import WSGIXMLRPCApplication as XmlRpcApplication

from mpd import MPDClient

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
        self.jsonrpc.methods[func.__name__] = func
        self.xmlrpcapp.dispatcher.register_function(func)
        return func

    def websocket(self, ws):
        while True:
            msg = ws.receive()
            if msg is not None:
                req = json.loads(msg)
                resp = self.jsonrpc(req)
                ws.send(json.dumps(resp))
            else: breaik

octavia = Octavia()

@octavia.register
def hello():
    return 'hello world'
 
if __name__ == '__main__':
    run(octavia.app, host='localhost', port=8080, server=GeventWebSocketServer)
