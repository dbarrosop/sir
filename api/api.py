from flask import g
import helpers.api

import yaml

def methods(request):
    with open('api/api_documentation.yaml', 'r') as stream:
        documentation = yaml.load(stream)

    result = []

    for app, endpoints  in documentation.iteritems():
        for endpoint in endpoints:
            for method in endpoint['methods']:
                result.append((endpoint['endpoint'], method['method']))

    parameters = {}
    return helpers.api.build_api_response(result, error=False, **parameters)
