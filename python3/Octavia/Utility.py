#!/usr/bin/python
import re

from bottle import request, response

def getinputsongs(allow_id=True, needed_keys=None):
    has_keys = lambda keys: True
    if needed_keys:
        has_keys = lambda keys: all([key in keys for key in needed_keys])
    is_song = lambda keys: 'id' in keys or 'file' in keys
    if not allow_id:
        is_song = lambda keys: 'file' in keys
    song_test = lambda song: (type(song) == dict and is_song(song.keys()) and
                              has_keys(song.keys())
    if not request.json or type(request.json) != list:
        return []
    return [song for song in request.json if sing_test(song)]

tokenizer = re.compile(r'(\d+)|(\D)').findall

naturalsort = (lambda item, key: 
  tuple(int(num) if num else aplha for num, aplha in tokenizer(get_key(item)))
)


