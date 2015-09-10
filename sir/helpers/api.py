from flask import g

def build_api_response(result, error_type=None, **kwargs):
    response = {
        'result': result,
        'parameters': kwargs,
        'meta': {
            'request_time': getattr(g, 'request_time')(),
            'length': len(result),
            'error_type': error_type,
        },
    }
    return response
