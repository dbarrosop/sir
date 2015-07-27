from flask import g

def build_api_response(result, error=False, **kwargs):
    response = {
        'result': result,
        'parameters': kwargs,
        'meta': {
            'request_time': getattr(g, 'request_time')(),
            'length': len(result),
            'error': error,
        },
    }
    return response
