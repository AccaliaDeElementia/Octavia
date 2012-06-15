#!/bin/bash
virtualenv2 .
source bin/activate

pip install bottle

pip install jsonrpc2

pip install wsgi-xmlrpc

pip install bottle-websocket
touch build/bottle-websocket/README.md
pip install bottle-websocket


pip install python-mpd2
