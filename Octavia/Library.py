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

