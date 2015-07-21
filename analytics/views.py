from flask import render_template
from flask import g


def _init_context_dates(db, request):
    context = dict()
    dates = db.get_dates()
    context['avail_start_time'] = dates[0].strftime('%Y-%m-%dT%H:%M')
    context['avail_end_time'] = dates[-1].strftime('%Y-%m-%dT%H:%M')
    context['start_time'] = request.form.get('start_time', dates[-25].strftime('%Y-%m-%dT%H:%M'))
    context['end_time'] = request.form.get('end_time', context['avail_end_time'])
    return context


def start_page(request):
    return render_template('analytics/start_page.html')


def offloaded_traffic(request):
    db = getattr(g, 'db', None)
    context = _init_context_dates(db, request)

    context['num_prefixes'] = int(request.form.get('num_prefixes', 1000))

    if request.method == 'GET':
        context['total_bytes'] = 0
        context['offloaded_bytes'] = 0
        context['percentage'] = 0.0
    elif request.method == 'POST':
        context['total_bytes'] = db.get_total_traffic(context['start_time'], context['end_time'])
        context['offloaded_bytes'
               ] = db.offloaded_bytes(context['num_prefixes'], context['start_time'], context['end_time'])
        context['percentage'] = float(context['offloaded_bytes']) * 100.0 / float(context['total_bytes'])

    return render_template('analytics/offloaded_traffic.html', **context)


def aggregate(request, field):
    db = getattr(g, 'db', None)
    context = _init_context_dates(db, request)

    context['flow_aggr'] = list()
    context['time_series'] = dict()
    context['time_series_times'] = list()

    if field == 'as':
        aggregate_method = db.aggregate_per_as
        timeseries_method = db.timeseries_per_as
        context['title'] = 'ASN\'s'
    elif field == 'prefix':
        aggregate_method = db.aggregate_per_prefix
        timeseries_method = db.timeseries_per_prefix
        context['title'] = 'Prefixes'

    if request.method == 'POST':
        context['time_series_times'] = db.get_dates_in_range(context['start_time'], context['end_time'])

        context['flow_aggr'] = aggregate_method(context['start_time'], context['end_time'])
        time_series = dict()
        for a in context['flow_aggr'][0:10]:
            time_series[a['key']] = timeseries_method(context['start_time'], context['end_time'], a['key'])

        context['time_series'] = time_series

    return render_template('analytics/analytics_aggregate.html', **context)


def simulate(request):
    db = getattr(g, 'db', None)
    context = _init_context_dates(db, request)

    context['num_prefixes'] = int(request.form.get('num_prefixes', 1000))
    context['time_series'] = dict()
    context['time_series_times'] = list()

    if request.method == 'POST':
        context['time_series_times'] = db.get_dates_in_range(context['start_time'], context['end_time'])

        time_series = dict()
        time_series['total_bytes'] = list()
        time_series['offloaded_bytes'] = list()

        for time_serie in context['time_series_times']:
            time_series['total_bytes'].append(db.get_total_traffic(time_serie, time_serie))
            time_series['offloaded_bytes'].append(db.offloaded_bytes(context['num_prefixes'], time_serie, time_serie))

        context['time_series'] = time_series

    return render_template('analytics/simulate.html', **context)
