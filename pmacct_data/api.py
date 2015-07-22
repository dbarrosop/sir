import helpers.api
from flask import g
from helpers.FSHelper import FSHelper


def get_dates(request):
    db = getattr(g, 'db')
    dates = [d.strftime('%Y-%m-%dT%H:%M:%S') for d in db.get_dates()]
    return helpers.api.build_api_response(result=dates, error=False)

def get_flows(request):
    db = getattr(g, 'db')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    flows = db.get_flows(start_time, end_time)
    return helpers.api.build_api_response(flows, error=False, start_time=start_time, end_time=end_time)

def get_bgp_prefixes(request):
    fs = FSHelper()
    date = request.args.get('date')
    bgp_prefixes = fs.get_bgp_prefixes(date)
    return helpers.api.build_api_response(bgp_prefixes, error=False, date=date)
