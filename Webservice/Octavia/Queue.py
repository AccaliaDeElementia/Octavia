#!/usr/bin/python2
import Octavia
app = Octavia.app

from flask import request, session, g, abort

def get_list():
    return [Octavia.filter_song(song) for song in
            g.client.playlistinfo()]

@app.route('/queue/')
@app.route('/queue/list')
@Octavia.WebMethod
def queue_list():
    return get_list()


@app.route('/queue/clear', methods=['POST'])
@Octavia.WebMethod
def queue_clear():
    g.client.clear()
    return get_list()

@app.route('/queue/delete', methods=['POST'])
@app.route('/queue/remove', methods=['POST'])
@Octavia.WebMethod
def queue_delete_songs():
    songs = Octavia.get_list_songs()
    queue = g.client.playlistinfo()
    ids = Octavia.filter_matches(songs, queue, lambda x, y: y['id'])
    g.client.command_list_ok_begin()
    for id_ in ids:
        g.client.deleteid(id_)
    g.client.command_list_end()
    return get_list()

@app.route('/queue/add', methods=['PUT'])
@Octavia.WebMethod
def queue_append_songs():
    songs = Octavia.get_list_songs(allow_id=False)
    g.client.command_list_ok_begin()
    for song in songs:
        g.client.add(song['file'])
    g.client.command_list_end()
    return get_list()

@app.route('/queue/add', methods=['POST'])
@Octavia.WebMethod
def queue_replace_songs():
    songs = Octavia.get_list_songs(allow_id=False)
    playing = g.client.status()['state'] == 'play'
    g.client.command_list_ok_begin()
    g.client.clear()
    for song in songs:
        g.client.add(song['file'])
    if playing:
        g.client.play()
    g.client.command_list_end()
    return get_list()

@app.route('/queue/shuffle', methods=['POST'])
@Octavia.WebMethod
def queue_shuffle():
    g.client.shuffle()
    return get_list()

@app.route('/queue/move', methods=['POST'])
@Octavia.WebMethod
def queue_move():
    songs = Octavia.get_list_songs(needed_keys=['index'])
    queue = g.client.playlistinfo()
    moves = Octavia.filter_matches(songs, queue,
                        lambda x, y: (y['id'], x['index']))
    g.client.command_list_ok_begin()
    for id_, dest in moves:
        g.client.moveid(id_, dest)
    g.client.command_list_end()
    return get_list()

@app.route('/queue/save/<name>', methods=['POST'])
@Octavia.WebMethod
def queue_save(name):
    g.client.save(name)
    return get_list()

@app.route('/queue/load/<name>', methods=['POST'])
@Octavia.WebMethod
def queue_load(name):
    playing = g.client.status()['state'] == 'play'
    g.client.command_list_ok_begin()
    g.client.clear()
    g.client.load(name)
    if playing:
        g.client.play()
    g.client.command_list_end()
    return get_list()

@app.route('/queue/load/<name>', methods=['PUT'])
@Octavia.WebMethod
def queue_load(name):
    g.client.load(name)
    return get_list()

@app.route('/queue/current')
@app.route('/queue/now_playing')
@Octavia.WebMethod
def queue_now_playing():
    return Octavia.filter_song(g.client.currentsong())
