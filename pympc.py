#!/usr/bin/python

import argparse
import json
from random import random
from xmlrpclib import ServerProxy as XmlRpcProxy
from urllib2 import Request, urlopen

def doXmlRpc(server, port, command, params):
    proxy = XmlRpcProxy('http://%s:%s/xml'%(server,port))
    return getattr(proxy, command)(*params)

def doJsonRpc(server, port, command, params):
    method = {'jsonrpc': '2.0', 'method': command, 'params':params, 'id':1}
    req = Request('http://%s:%s/json'%(server,port),json.dumps(method),{'Content-Type': 'application/json'})
    resp = json.loads(urlopen(req).read())
    return resp.get('result', resp)

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--server', default='localhost')
parser.add_argument('-p', '--port', type=int, default=8080)
parser.add_argument('-J', '--JSON', action='store_const', const='JSON', dest='type')
parser.add_argument('-X', '--XML', action='store_const', const='XML', dest='type')
parser.add_argument('command')
parser.add_argument('params', nargs='*')

args = parser.parse_args()

method = {
    'JSON': doJsonRpc,
    'XML': doXmlRpc,
}.get(args.type, doJsonRpc)
result = method(args.server, args.port, args.command, args.params)
print json.dumps(result, indent=2)
