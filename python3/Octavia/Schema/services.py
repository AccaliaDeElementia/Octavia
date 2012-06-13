#!/usr/bin/python

import json
import validictory

application = {
    'title': 'Application',
    'description': 'Application Information',
    'type': 'object',
    'properties': {
        'name': {
            'description': 'Application Name',
            'type': 'string',
            'blank': False,
        },
        'version': {
            'description': 'Application Version',
            'type': 'string',
            'blank': False,
        },
        'author': {
            'description': 'Application Author',
            'type': 'string',
            'blank': False,
        },
        'website': {
            'description': 'Application Homepage',
            'type': ['string', 'null'],
            'blank': True,
        },
        'license': {
            'description': 'Application License Name',
            'type': 'string',
            'blank': False,
        },
        'licenseuri': {
            'description': 'Web Address of Full Application License',
            'type': 'string',
            'blank': False,
        },
    }
}



header = {
    'title': 'Header',
    'description': 'Request/Response Header',
    'type': 'object',
    'parameters': {
        'name': { 'type': 'string' },
        'style': { 'enum' : ['header'] },
        'value_type': { 'enum': ['string', 'int', 'number', 'boolean'] },
        'value_description': { 'type': 'string' }
    }
}

query_param = {
    'title': 'QueryParam',
    'description': 'Request Query String Parameter',
    'type': 'object',
    'parameters': {
        'name': { 'type': 'string' },
        'style': { 'enum' : ['query'] },
        'valuetype': { 'enum': ['string', 'int', 'number', 'boolean'] },
        'description': { 'type': 'string' }
    }
}

content = {
    'title': 'Content',
    'description': 'RequestResponse Content',
    'type': 'object',
    'properties': {
        'description': {
            'description': 'Description of Content Object',
            'type': 'string',
        },
        'schema': {
            'description': 'Scema Defining Content',
            'type': 'object'
        }
    }
}

web_request = {
    'title': 'WebRequest',
    'description': 'Request sent to Web Method',
    'type': 'object',
    'properties': {
        'parameters': {
            'description': 'Request Parameters',
            'type': 'array',
            'items': { 'type': [ header, query_param ]}
        },
        'content': {
            'description': 'Request Content',
            'type': [ 'null', content ]
        }
    }
}

web_response = {
    'title': 'WebResponse',
    'description': 'Response Generated by Web Method',
    'type': 'object',
    'properties': {
        'status': {
            'description': 'HTTP Response Code as per RFC 2616 sec. 9',
            'type': 'array',
            'items': {
                'enum': [200, 201, 202, 203, 204, 205, 206, 300, 301, 302, 303, 
                         304, 305, 307, 400, 401, 403, 405, 406, 407, 408, 409,
                         410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502,
                         503, 504, 505, '*', '2xx', '3xx', '4xx', '5xx']
            }
        },
        'description': {
            'type': 'string',
            'description': 'Description of Request/Response Object'
        },
        'headers': {
            'description': 'Headers set By Web Method',
            'type': 'array',
            'items': header
        },
        'content': {
            'description': 'response Content',
            'type': [ 'null', content ]
        }
    }
}

web_method = {
    'title': 'WebMethod',
    'description': 'Web Method Definition',
    'type': 'object',
    'properties': {
        'name': {
            'description': 'Method Name',
            'type': 'string'
        },
        'description': {
            'description': 'Method Description',
            'type': 'string',
            'required': False
        },
        'actions': {
            'description': ('HTTP Methods acted on by Method, ' +
                           'as per RFC 2616 sec. 9'),
            'type': 'array',
            'items': {
                'type': 'string',
                'enum': ['OPTIONS', 'HEAD', 'GET', 'PUT', 'POST', 'DELETE']
            }
        },
        'request': { 'type': web_request },
        'response': { 'type': 'array', 'items': web_response, 'minItems': 1 }
    }
}

resource = {
    'title': 'WebResource',
    'description': 'Web Resource Definition',
    'type': 'object',
    'properties': {
        'path': {
            'description': 'Resource Path Relative to Service BaseUri',
            'type': 'string',
            'pattern': '^(/)?([^/]+/)*([^/]+(/)?)?$'
        },
        'methods': {
            'description': 'Web Methods that act on the Resource',
            'type': 'array',
            'items': web_method,
        }
    }
}

services = {
    'title': 'Services',
    'description': 'Services Offered by Application',
    'type': 'object',
    'properties': {
        'baseuri': {
            'description': 'Base URI for all Services',
            'type': 'string',
            'format': 'uri',
        },
        'resources': {
            'description': 'Resources Exposed by Service',
            'type': 'array',
            'items': resource,
        }
    }
}

services_schema = {
    'title': 'Services',
    'description': 'JSON Web Service Description',
    'type': 'object',
    'properties': {
        'application': { 'type': application },
        'services': { 'type': services }
    }
}

if __name__ == '__main__':
    print (json.dumps(services_schema, indent=4))
