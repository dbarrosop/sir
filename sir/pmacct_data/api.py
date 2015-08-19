import sir.helpers.api
from flask import g


def get_dates(request):
    db = getattr(g, 'db')
    dates = [d.strftime('%Y-%m-%dT%H:%M:%S') for d in db.get_dates()]
    return sir.helpers.api.build_api_response(result=dates, error=False)


def get_flows(request):
    db = getattr(g, 'db')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    flows = db.get_flows(start_time, end_time)
    return sir.helpers.api.build_api_response(flows, error=False, start_time=start_time, end_time=end_time)


def get_bgp_prefixes(request):
    fs = getattr(g, 'fs')
    date = request.args.get('date')
    bgp_prefixes = fs.get_bgp_prefixes(date)
    return sir.helpers.api.build_api_response(bgp_prefixes, error=False, date=date)


def get_raw_bgp(request):
    fs = getattr(g, 'fs')
    date = request.args.get('date')
    bgp_prefixes = fs.get_raw_bgp(date)
    return sir.helpers.api.build_api_response(bgp_prefixes, error=False, date=date)


def purge_bgp(request):
    fs = getattr(g, 'fs')
    older_than = request.args.get('older_than')
    purged_bgp_tables = fs.purge_bgp(older_than)
    return sir.helpers.api.build_api_response(purged_bgp_tables, error=False, older_than=older_than)


def purge_flows(request):
    db = getattr(g, 'db')
    older_than = request.args.get('older_than')
    purged_flows = db.purge_flows(older_than)
    return sir.helpers.api.build_api_response(purged_flows, error=False, older_than=older_than)
