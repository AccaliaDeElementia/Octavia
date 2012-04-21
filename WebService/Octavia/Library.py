#!/usr/bin/python2
import Octavia
app = Octavia.app

from datetime import datetime

from mpd import MPDClient, CommandError
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

@app.route('/library/')
@app.route('/library/list/')
@app.route('/library/list/<path:directory>')
@Octavia.WebMethod
def library(directory = ''):
    dir_ = g.client.lsinfo(directory)
    results = []
    for item in dir_:
        keys = item.keys()
        if 'directory' in keys:
            results.append(item)
        elif 'file' in keys:
            results.append(Octavia.filter_song(item))
    return results

@app.route('/library/tree/')
@app.route('/library/tree/<path:directory>')
@Octavia.WebMethod
def tree(directory=''):
    def rtree (directory):
        dir_ = g.client.lsinfo(directory)
        contents = []
        for item in dir_:
            keys = item.keys()
            if 'directory' in keys:
                contents.append(rtree(item['directory']))
            elif 'file' in keys:
                contents.append(Octavia.filter_song(item))
        return {
            'directory': directory,
            'name': directory.rsplit('/',1)[-1],
            'contents': contents
        }

    return rtree(directory)
