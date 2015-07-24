# -*- coding: utf-8 -*-

# TODO UI for searching
# TODO Local Architecture
# TODO Features, README, use cases, etc...
# TODO Global Architecture
# TODO Expose raw flows, delete flows
# TODO Expose raw BGP, delete raw BGP files
# TODO UI to Add, Edit, delete variables
# TODO metrics
# TODO Improve building the response of the API and documentation
# TODO Catch errors in API
# TODO Catch errors in logging
# TODO Catch errors in authentication???

from helpers.SQLite3Helper import SQLite3Helper
from helpers.FSHelper import FSHelper

import variables.api
import variables.views

import analytics.api
import analytics.views

import api.views

import pmacct_data.api

from flask import Flask, request, g, jsonify, render_template

import time

app = Flask(__name__)
app.config.from_object('settings')

###################
###################
#  BASIC  #########
###################
###################


@app.before_request
def before_request():
    g.db = SQLite3Helper(app.config['DATABASE'])
    g.db.connect()
    g.request_start_time = time.time()
    g.request_time = lambda: float("%.5f" %
                                   (time.time() - g.request_start_time))
    g.fs = FSHelper(app.config['BGP_FOLDER'])


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/', strict_slashes=False)
def start_page():
    return render_template('basic/start_page.html')

###################
###################
#  ANALYTICS  #####
###################
###################


@app.route('/analytics', strict_slashes=False)
def analytics_view_help():
    return analytics.views.start_page(request)


@app.route('/analytics/offloaded_traffic', methods=['GET', 'POST'])
def analytics_view_offloaded_traffic():
    return analytics.views.offloaded_traffic(request)


@app.route('/analytics/aggregate_per_as', methods=['GET', 'POST'])
def analytics_view_aggregate_per_as():
    return analytics.views.aggregate(request, 'as')


@app.route('/analytics/aggregate_per_prefix', methods=['GET', 'POST'])
def analytics_view_aggregate_per_prefix():
    return analytics.views.aggregate(request, 'prefix')


@app.route('/analytics/simulate', methods=['GET', 'POST'])
def analytics_view_simulate():
    return analytics.views.simulate(request)


@app.route('/api/v1.0/analytics/top_prefixes', methods=['GET'])
def analytics_api_top_prefixes():
    return jsonify(analytics.api.top_prefixes(request))


@app.route('/api/v1.0/analytics/top_asns', methods=['GET'])
def analytics_api_top_asns():
    return jsonify(analytics.api.top_asns(request))


@app.route('/api/v1.0/analytics/find_prefix/<prefix>/<pl>', methods=['GET'])
def analytics_api_find_prefix(prefix, pl):
    return jsonify(analytics.api.find_prefix(request, u'{}/{}'.format(prefix, pl)))


@app.route('/analytics/find_prefix', methods=['GET', 'POST'])
def analytics_view_find_prefix():
    return analytics.views.find_prefix(request)


@app.route('/api/v1.0/analytics/find_prefixes_asn/<asn>', methods=['GET'])
def analytics_api_find_prefixes_asn(asn):
    return jsonify(analytics.api.find_prefixes_asn(request, asn))


@app.route('/analytics/find_prefixes_asn', methods=['GET', 'POST'])
def analytics_view_find_prefix_asn():
    return analytics.views.find_prefix_asn(request)


###################
###################
#  API  ###########
###################
###################


@app.route('/api/documentation', strict_slashes=False)
def api_help():
    return api.views.start_page(request)


###################
###################
#  VARIABLES  #####
###################
###################


@app.route('/variables/browse', methods=['GET'])
def browse_view_variables():
    return variables.views.browse_variables(request)

'''
@app.route('/variables/edit/<category>/<name>', methods=['GET', 'POST', 'DELETE'])
def edit_variable(category, name):
    return variables.views.edit_variable(request, category, name)
'''


@app.route('/api/v1.0/variables', methods=['GET', 'POST'])
def variables_api_variables():
    return jsonify(variables.api.variables(request))


@app.route('/api/v1.0/variables/categories', methods=['GET'])
def variables_api_category():
    return jsonify(variables.api.variables_category(request))


@app.route('/api/v1.0/variables/categories/<category>', methods=['GET'])
def variables_api_filter_by_category(category):
    return jsonify(variables.api.variables_filter_by_category(request, category))


@app.route('/api/v1.0/variables/categories/<category>/<name>', methods=['GET', 'PUT', 'DELETE'])
def variables_api_name(category, name):
    return jsonify(variables.api.api_variables_name(request, category, name))

###################
###################
#  PMACCT_DATA  ###
###################
###################


@app.route('/api/v1.0/pmacct/dates', methods=['GET'])
def pmacct_data_api_get_dates():
    return jsonify(pmacct_data.api.get_dates(request))


@app.route('/api/v1.0/pmacct/flows', methods=['GET'])
def pmacct_data_api_get_flows():
    return jsonify(pmacct_data.api.get_flows(request))


@app.route('/api/v1.0/pmacct/bgp_prefixes', methods=['GET'])
def pmacct_data_api_get_bgp_prefixes():
    return jsonify(pmacct_data.api.get_bgp_prefixes(request))


if __name__ == '__main__':
    app.run(app.config['BIND_IP'], app.config['PORT'])
