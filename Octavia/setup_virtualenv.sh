#!/bin/bash
function fix2to3 {
    tree -inf "$1"|egrep py$|while read i; do 2to3 -w $i; done
}

virtualenv .
source bin/activate

pip install bottle

pip install jsonrpc2
fix2to3 "lib/python3.2/site-packages/jsonrpc2"

pip install wsgi-xmlrpc
fix2to3 "lib/python3.2/site-packages/wsgi-xmlrpc"

pip install bottle-websocket
touch "build/bottle-websocket/README.md"
pip install bottle-websocket
fix2to3 "build/gevent"
pip install bottle-websocket
