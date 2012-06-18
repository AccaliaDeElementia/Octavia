#!/usr/bin/python
from Octavia import octavia
from bottle import run
from bottle.ext.websocket import GeventWebSocketServer

if __name__ == '__main__':
    run(octavia.app, host='localhost', port=8080, server=GeventWebSocketServer)
