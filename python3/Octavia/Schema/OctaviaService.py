#!/usr/bin/python

from songs import songlist

octavia_service = {
    'application': {
        'name': 'Octavia',
        'version': '0.5.0Alpha',
        'author': 'Accalia de Elementia',
        'website': None,
        'license': 'Creative Commons Attribution 3.0 Unported',
        'licenseuri': 'https://creativecommons.org/licenses/by/3.0/'
    },
    'services': {
        'baseuri': 'https://octavia/darkstaranime.com',
        'resources': [
            {
                'path': '/queue',
                'methods': [
                    {
                        'name': 'QueueList',
                        'description': 'List Songs in the Play Queue',
                        'actions': ['HEAD', 'GET'],
                        'request': {
                            'parameters': [],
                            'content': None
                        },
                        'response': [
                            {
                                'status': [200],
                                'description': 'List of Songs in Play Queue',
                                'headers': [
                                    {
                                        'name': 'ETag',
                                        'style': 'header',
                                        'valuetype': 'string',
                                        'description': 'ETag  Header'
                                    }
                                ],
                                'content': {
                                    'description': 'List of Songs'
                    }
                ]
            }
        ]
    }
}

if __name__ == '__main__':
    from services import services_schema
    import validictory


    validictory.validate(octavia_service, services_schema)
