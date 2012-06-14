#!/usr/bin/python

from bottle import Bottle, run
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

from jsonrpc2 import JsonRpcApplication
from wsgi_xmlrpc import WSGIXMLRPCApplication as XmlRpcApplication



def hello():
    return 'hello world'
 
jsonrpc = JsonRpcApplication(rpcs={'hello': hello})
xmlrpc = XmlRpcApplication(methods=[hello])

app = Bottle()
app.mount('/json', jsonrpc)
app.mount('/xml', xmlrpc)

@app.route('/hello')
def hello_str():
    return 'hello World!'

@app.get('/ws', apply=[websocket])
def echo_srv(ws):
    while True:
        msg = ws.receive()
        if msg is not None:
            ws.send(msg)
        else: break


if __name__ == '__main__':
    run(app, host='localhost', port=8080, server=GeventWebSocketServer)
