#!/usr/bin/python
from Octavia import octavia, mpc, filter_song

@octavia.register
def libraryList(directory='/'):
    '''Return a list of the contents of a directory in the music library.'''
    r = []
    for item in mpc.client.lsinfo(directory):
        keys = item.keys()
        if 'playlist' in keys:
            r.append({'playlist':item['playlist']})
        elif 'directory' in keys:
            r.append({'directory':item['directory']})
        else:
            r.append(filter_song(item))
    return r

@octavia.register
def libraryListAll():
    '''Return a list of all songs in the music library.'''
    return [filter_song(item) for item in mpc.client.listallinfo()]

@octavia.register
def libraryStats():
    '''Return basic statistics about the music library.'''
    return {x: int(y) for x,y in mpc.client.stats().items()}
    
@octavia.register
def libraryFind(type_, needle):
    '''Return a list of songs where [needle] exactly matches metadata [type_].'''
    return [filter_song(item) for item in mpc.client.find(type_, needle)]

@octavia.register
def librarySearch(type_, needle):
    '''Return a list of songs where metadata [type_] contains [needle].'''
    return [filter_song(item) for item in mpc.client.search(type_, needle)]

@octavia.register
def libraryUpdate(path='/'): 
    '''Look for changes in music library, starting at [path].'''
    return mpc.client.update()

@octavia.register
def libraryRescan(path='/'):
    '''Rescan music library, starting at [path].'''
    return mpc.client.rescan(path)
