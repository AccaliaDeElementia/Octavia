#!/usr/bin/python2
import Octavia
app = Octavia.app

import json

from mpd import MPDClient, CommandError
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

@app.teardown_request
def disconnect(error):
    try:
        g.client.disconnect()
    except:
        pass




@app.route('/playlist/')
@app.route('/playlist/list')
@Octavia.WebMethod
def list_playlist():
    playlist = g.client.playlistinfo()
    return [Octavia.filter_song(song) for song in playlist]

@app.route('/playlist/current')
@Octavia.WebMethod
def show_current():
    return g.client.currentsong()

@app.route('/playlist/save', methods=['POST'])
@Octavia.WebMethod
def save_paylist():
    data = Octavia.get_data()
    if 'name' not in data.keys():
        abort(400, "name not specified")
    g.client.save(data['name'])
    return True

@app.route('/playlists/')
@Octavia.WebMethod
def list_playlists():
    data = g.client.listplaylists()
    return [playlist['playlist'] for playlist in data]

@app.route('/playlists/<name>')
@Octavia.WebMethod
def show_playlist(name):
    data = g.client.listplaylistinfo(name)
    return [Octavia.filter_song(song) for song in data]

@app.route('/playlists/<name>', methods=['DELETE'])
@Octavia.WebMethod
def delete_paylist(name):
    g.client.rm(name)
    return True


