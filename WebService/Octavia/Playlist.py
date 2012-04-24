#!/usr/bin/python2
import Octavia
app = Octavia.app

from flask import request, session, g, abort

def filter_matches(needles, haystack, formatter):
    results = []
    matches = lambda a, b: (str(a['id']) == b['id'] if 'id' in a.keys()
                            else a['file'] == b['file'])
    for needle in needles:
        results += [formatter(needle, straw) for straw in haystack if
                    matches(needle, straw)]
    if len(results) < 1:
        abort(404, 'No songs matching criteria found')
    return results

def get_playlists():
    return Octavia.sort_list(g.client.listplaylists(),
                             lambda p: p['playlist'])

@app.route('/playlist')
@Octavia.WebMethod
def list_playlists():
    return get_playlists()

@app.route('/playlist/<name>')
@Octavia.WebMethod
def list_playlist(name):
    return [Octavia.filter_song(song) for song in
            g.client.listplaylistinfo(name)]

@app.route('/playlist/<name>', methods=['DELETE'])
@Octavia.WebMethod
def delete_playlist(name):
    g.client.rm(name)
    return get_playlists()

@app.route('/playlist/<name>/add', methods=['PUT'])
@Octavia.WebMethod
def add_playlist (name):
    songs = Octavia.get_list_songs(allow_id=False)
    g.client.command_list_ok_begin()
    for song in songs:
        g.client.playlistadd(name, song['file'])
    g.client.command_list_end()
    return list_playlist(name)
    
@app.route('/playlist/<name>/add', methods=['POST'])
@Octavia.WebMethod
def replace_playlist (name):
    songs = Octavia.get_list_songs(allow_id=False)
    g.client.command_list_ok_begin()
    g.client.playlistclear(name)
    for song in songs:
        g.client.playlistadd(name, song['file'])
    g.client.command_list_end()
    return list_playlist(name)


@app.route('/playlist/<name>/move', methods=['POST'])
@Octavia.WebMethod
def move_playlist(name):
    songs = Octavia.get_list_songs(neede_keys=['index'])
    playlist = g.client.listplaylistinfo(name)
    moves = Octavia.filter_matches(songs, playlist, 
                                   lambda x, y: (y['id'], x['index']))
    g.client.command_list_ok_begin()
    for id_, dest in moves:
        g.client.playlistmove(id_, dest)
    g.client.command_list_end()
    return list_playlist(name)

