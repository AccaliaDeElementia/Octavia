#!/usr/bin/python
from Octavia import octavia, filter_song, mpc

@octavia.register
def playlistList():
    '''Return a list of stored playlist names.'''
    return [x['playlist'] for x in mpc.client.listplaylists()]

@octavia.register
def playlistInfo(name):
    '''Return a list of songs contained in stored playlist [name].'''
    return [filter_song(s) for s in mpc.client.listplaylistinfo(name)]

@octavia.register
def playlistAdd(name, path):
    '''Add [path] to stored playlist [name] and return updated playlist.'''
    mpc.client.playlistadd(name, path)
    return playlistInfo(name)

@octavia.register
def playlistReplace(name, path):
    '''replace contents of stored playlist [name] with [path] and return updated playlist.'''
    playlistClear(name)
    mpc.client.playlistadd(name, path)
    return playlistInfo(name)

@octavia.register
def playlistRemove(name, songid):
    '''Remove [songid] from stored playlist [name] and return updated playlist.'''
    mpc.client.playlistdelete(name, songid)
    return playlistInfo(name)

@octavia.register
def playlistClear(name):
    '''Clear contents of stored playlist [name] and return updated playlist.'''
    mpc.client.playlistclear(name)
    return playlistInfo(name)

@octavia.register
def playlistMove(name, from_, to_):
    '''Move position [from_] to position [to_] in stored playlist [name] and return updated playlist.'''
    mpc.client.playlistmove(name, from_, to_)
    return playlistInfo(name)

@octavia.register
def playlistRename(oldname, newname):
    '''Rename stored playlist [oldname] to [newname].'''
    return mpc.client.rename(oldname, newname)

@octavia.register
def playlistDelete(name):
    '''Delete stored playlist [name].'''
    return mpc.client.rm(name)

