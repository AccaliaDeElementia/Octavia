#!/usr/bin/python
from Octavia import octavia, filter_song, mpc

@octavia.register
def queueList(sid=None):
    if sid is None:
        songs = mpc.client.playlistinfo()
    else:
        songs = mpc.client.playlistinfo(sid)
    return [filter_song(song) for song in songs]

@octavia.register
def queueCurrent():
    return filter_song(mpc.client.currentsong())
