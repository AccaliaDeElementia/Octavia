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

@octavia.register
def queueNext():
    return mpc.client.next()

@octavia.register
def queuePrev():
    return mpc.client.previous()

@octavia.register
def queuePlay(sid=None)
    if sid is None:
        return mpc.client.play()
    return mpd.client.play(sid)

@octavia.register
def queuePause():
    return mpc.client.pause(1)

@octavia.register
def queueStop():
    return mpc.client.stop()
