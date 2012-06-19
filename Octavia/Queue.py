#!/usr/bin/python
from Octavia import octavia, filter_song, mpc

@octavia.register
def queueList():
    '''Return a list of songs in the play queue.'''
    songs = mpc.client.playlistinfo()
    return [filter_song(song) for song in songs]

@octavia.register
def queueCurrent():
    '''Return the currently playing song.'''
    return filter_song(mpc.client.currentsong())

@octavia.register
def queueNext():
    '''Advance the play queue by one song.'''
    mpc.client.next()
    return queueCurrent()

@octavia.register
def queuePrev():
    '''Rewind the play queue by one song.'''
    mpc.client.previous()
    return queueCurrent()

@octavia.register
def queuePlay(position=None):
    '''Resume playback of play queue, optionally at [position].'''
    if position is None:
        mpc.client.play()
    else:
        mpd.client.play(position)
    return queueCurrent()

@octavia.register
def queuePause():
    '''Pause playback of play queue.'''
    mpc.client.pause(1)
    return queueCurrent()

@octavia.register
def queueToggle ():
    '''Toggle play/pause of play queue.'''
    if mpc.client.status().get('state','') == 'play':
        mpc.client.pause(1)
    else:
        mpc.client.play()
    return queueCurrent()

@octavia.register
def queueStop():
    '''Stop playback of play queue.'''
    mpc.client.stop()
    return queueCurrent()

@octavia.register
def queueClear():
    '''Clear play queue and return new play queue.'''
    mpc.client.clear()
    return queueList()

@octavia.register
def queueRandomize():
    '''Randomize order of play queue and return new play queue.'''
    mpc.client.shuffle()
    return queueList()

@octavia.register
def queueAdd (path, position=None):
    '''Add [path] to play queue, optionally starting at [position], and return new play queue.'''
    if position is None:
        mpc.client.addid(path)
    else:
        mpc.client.addid(path, position)
    return queueList()

@octavia.register
def queueReplace (path):
    '''Replace contents of play queue with [path] and return new play queue.'''
    playing = mpc.client.status().get('state','') == 'play'
    mpc.client.clear()
    mpc.client.addid(path)
    if playing:
        mpc.client.play()
    return queueList()

@octavia.register
def queueSave(name):
    '''Save play queue as playlist [name].'''
    return mpc.client.save(name)

@octavia.register
def queueLoad(name):
    '''Load play queue from playlist [name] and return new play queue.'''
    playing = mpc.client.status().get('state','') == 'play'
    mpc.client.load(name)
    if playing:
        mpc.client.play()
    return queueList()

@octavia.register
def queueRemove(songid):
    '''Remove song [songid] from the play queue and return new play queue.'''
    mpc.client.deleteid(songid)
    return queueList()

@octavia.register
def queueMove(fromid, position):
    '''Move song [songid] to [position] and return new play queue.'''
    mpc.client.moveid(fromid, position)
    return queueList()
