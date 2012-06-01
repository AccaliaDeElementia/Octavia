#!/usr/bin/python
import Octavia
from bottle import run

run(Octavia.app, host='localhost', port=8000, reloader=True)
