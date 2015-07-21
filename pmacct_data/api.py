import helpers.api
from flask import g

def get_dates(request):
    db = getattr(g, 'db')
    dates = db.get_dates()
    return helpers.api.build_api_response(result=dates, error=False)

def get_flows(request):
    db = getattr(g, 'db')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    flows = db.get_flows(start_time, end_time)
    return helpers.api.build_api_response(flows, error=False, start_time=start_time, end_time=end_time)
