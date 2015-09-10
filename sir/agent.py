# -*- coding: utf-8 -*-
"""
SIR Agent
"""

from sir.helpers.SQLite3Helper import SQLite3Helper
from sir.helpers.FSHelper import FSHelper

import sir.variables.api
import sir.variables.views

import sir.analytics.api
import sir.analytics.views

import sir.api.views

import sir.pmacct_data.api

from flask import Flask, request, g, jsonify, render_template

import time

app = Flask(__name__)
app.config.from_envvar('SIR_SETTINGS', silent=True)

###################
###################
#  BASIC  #########
###################
###################


@app.before_request
def before_request():
    """
    before_request
    """
    g.db = SQLite3Helper(app.config['DATABASE'])
    g.db.connect()
    g.request_start_time = time.time()
    g.request_time = lambda: float("%.5f" % (time.time() - g.request_start_time))
    g.fs = FSHelper(app.config['BGP_FOLDER'])


@app.teardown_request
def teardown_request(exception):
    """
    teardown_request
    """
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/', strict_slashes=False)
def start_page():
    """
    start_page
    """
    return render_template('basic/start_page.html')

###################
###################
#  ANALYTICS  #####
###################
###################


@app.route('/analytics', strict_slashes=False)
def analytics_view_help():
    """
    analytics_view_help
    """
    return sir.analytics.views.start_page(request)


@app.route('/analytics/offloaded_traffic', methods=['GET', 'POST'])
def analytics_view_offloaded_traffic():
    """
    analytics_view_offloaded_traffic
    """
    return sir.analytics.views.offloaded_traffic(request)


@app.route('/analytics/aggregate_per_as', methods=['GET', 'POST'])
def analytics_view_aggregate_per_as():
    """
    analytics_view_aggregate_per_as
    """
    return sir.analytics.views.aggregate(request, 'as')


@app.route('/analytics/aggregate_per_prefix', methods=['GET', 'POST'])
def analytics_view_aggregate_per_prefix():
    """
    analytics_view_aggregate_per_prefix
    """
    return sir.analytics.views.aggregate(request, 'prefix')


@app.route('/analytics/simulate', methods=['GET', 'POST'])
def analytics_view_simulate():
    """
    analytics_view_simulate
    """
    return sir.analytics.views.simulate(request)


@app.route('/api/v1.0/analytics/top_prefixes', methods=['GET'])
def analytics_api_top_prefixes():
    """
    analytics_api_top_prefixes
    """
    return jsonify(sir.analytics.api.top_prefixes(request))


@app.route('/api/v1.0/analytics/top_asns', methods=['GET'])
def analytics_api_top_asns():
    """
    analytics_api_top_asns
    """
    return jsonify(sir.analytics.api.top_asns(request))


@app.route('/api/v1.0/analytics/find_prefix/<prefix>/<pl>', methods=['GET'])
def analytics_api_find_prefix(prefix, prefix_length):
    """
    analytics_api_find_prefix
    """
    return jsonify(sir.analytics.api.find_prefix(request, u'{}/{}'.format(prefix, prefix_length)))


@app.route('/analytics/find_prefix', methods=['GET', 'POST'])
def analytics_view_find_prefix():
    """
    analytics_view_find_prefix
    """
    return sir.analytics.views.find_prefix(request)


@app.route('/api/v1.0/analytics/find_prefixes_asn/<asn>', methods=['GET'])
def analytics_api_find_prefixes_asn(asn):
    """
    analytics_api_find_prefixes_asn
    """
    return jsonify(sir.analytics.api.find_prefixes_asn(request, asn))


@app.route('/analytics/find_prefixes_asn', methods=['GET', 'POST'])
def analytics_view_find_prefix_asn():
    """
    analytics_view_find_prefix_asn
    """
    return sir.analytics.views.find_prefix_asn(request)

###################
###################
#  VARIABLES  #####
###################
###################


@app.route('/variables/browse', methods=['GET'])
def browse_view_variables():
    """
    browse_view_variables
    """
    return sir.variables.views.browse_variables(request)


'''
@app.route('/variables/edit/<category>/<name>', methods=['GET', 'POST', 'DELETE'])
def edit_variable(category, name):
    return variables.views.edit_variable(request, category, name)
'''


@app.route('/api/v1.0/variables', methods=['GET', 'POST'])
def variables_api_variables():
    """
    variables_api_variables
    """
    return jsonify(sir.variables.api.variables(request))


@app.route('/api/v1.0/variables/categories', methods=['GET'])
def variables_api_category():
    """
    variables_api_category
    """
    return jsonify(sir.variables.api.variables_category(request))


@app.route('/api/v1.0/variables/categories/<category>', methods=['GET'])
def variables_api_filter_by_category(category):
    """
    variables_api_filter_by_category
    """
    return jsonify(sir.variables.api.variables_filter_by_category(request, category))


@app.route('/api/v1.0/variables/categories/<category>/<name>', methods=['GET', 'PUT', 'DELETE'])
def variables_api_name(category, name):
    """
    variables_api_name
    """
    return jsonify(sir.variables.api.api_variables_name(request, category, name))

###################
###################
#  PMACCT_DATA  ###
###################
###################


@app.route('/api/v1.0/pmacct/dates', methods=['GET'])
def pmacct_data_api_get_dates():
    """
    pmacct_data_api_get_dates
    """
    return jsonify(sir.pmacct_data.api.get_dates(request))


@app.route('/api/v1.0/pmacct/flows', methods=['GET'])
def pmacct_data_api_get_flows():
    """
    pmacct_data_api_get_flows
    """
    return jsonify(sir.pmacct_data.api.get_flows(request))


@app.route('/api/v1.0/pmacct/raw_bgp', methods=['GET'])
def pmacct_data_api_get_raw_bgp():
    """
    pmacct_data_api_get_raw_bgp
    """
    return jsonify(sir.pmacct_data.api.get_raw_bgp(request))


@app.route('/api/v1.0/pmacct/bgp_prefixes', methods=['GET'])
def pmacct_data_api_get_bgp_prefixes():
    """
    pmacct_data_api_get_bgp_prefixes
    """
    return jsonify(sir.pmacct_data.api.get_bgp_prefixes(request))


@app.route('/api/v1.0/pmacct/purge_bgp', methods=['GET'])
def pmacct_data_api_purge_bgp():
    """
    pmacct_data_api_purge_bgp
    """
    return jsonify(sir.pmacct_data.api.purge_bgp(request))


@app.route('/api/v1.0/pmacct/purge_flows', methods=['GET'])
def pmacct_data_api_purge_flows():
    """
    pmacct_data_api_purge_flows
    """
    return jsonify(sir.pmacct_data.api.purge_flows(request))


if __name__ == '__main__':
    app.run(app.config['BIND_IP'], app.config['PORT'])
