#!/usr/bin/python
song = {
    'title': 'Song',
    'description': 'Information regarding MPD Songs',
    'type': 'object',
    'properties': {
        'album': { 
            'descripton': 'Song Album Name'
            'type': 'string',
            'blank': True,
        },
        'title': { 
            'description': 'Song Title',
            'type': 'string',
            'blank': True,
        },
        'artist': { 
            'description': 'Song Artist',
            'type': 'string',
            'blank': True,
        },
        'track': {
            'description': 'Track Number',
            'type': 'integer',
            'minimum': 0,
            'required': False,
        },
        'time': { 
            'description': 'Playtime in Seconds',
            'type': 'integer',
            'minimum': 0,
        },
        'file': { 
            'description': 'Song File Location',
            'type': 'sting',
            'blank': False,
        },
        'id': { 
            'description': 'Playlist Speciffic Id',
            'type': 'integer',
            'minimum': 0,
            'required': False,
        }
    }
}
file_song = {
    'title': 'Request Song by Path',
    'description': 'A Song Identified by Path',
    'type': 'object',
    'properties': {
        'file': { 
            'description': 'Song File Location',
            'type': 'sting',
            'blank': False,
        },
    }
}
id_song = {
    'title': 'Request Song by Id',
    'description': 'A Song Identified by Playlist Id',
    'type': 'object',
    'properties': {
        'file': { 
            'description': 'Song File Location',
            'type': 'sting',
            'blank': False,
        },
    }
}

song_list = {
    'title': 'Song List',
    'description': 'List of MPD Songs',
    'type': 'array',
    'items': song
}
