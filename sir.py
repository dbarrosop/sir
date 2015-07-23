# -*- coding: utf-8 -*-

# TODO Expose raw flows, delete flows
# TODO Expose raw BGP, delete raw BGP files
# TODO UI to Add, Edit, delete variables
# TODO metrics
# TODO Improve building the response of the API and documentation
# TODO Catch errors in API
# TODO Catch errors in logging
# TODO Catch errors in authentication???

from helpers.SQLite3Helper import SQLite3Helper

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
def analytics_help():
    return analytics.views.start_page(request)


@app.route('/analytics/offloaded_traffic', methods=['GET', 'POST'])
def analytics_offloaded_traffic():
    return analytics.views.offloaded_traffic(request)


@app.route('/analytics/aggregate_per_as', methods=['GET', 'POST'])
def analytics_aggregate_per_as():
    return analytics.views.aggregate(request, 'as')


@app.route('/analytics/aggregate_per_prefix', methods=['GET', 'POST'])
def analytics_aggregate_per_prefix():
    return analytics.views.aggregate(request, 'prefix')


@app.route('/analytics/simulate', methods=['GET', 'POST'])
def analytics_simulate():
    return analytics.views.simulate(request)


@app.route('/api/v1.0/analytics/top_prefixes', methods=['GET'])
def api_top_prefixes():
    return jsonify(analytics.api.top_prefixes(request))


@app.route('/api/v1.0/analytics/top_asns', methods=['GET'])
def api_top_asns():
    return jsonify(analytics.api.top_asns(request))

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
def browse_variables():
    return variables.views.browse_variables(request)

'''
@app.route('/variables/edit/<category>/<name>', methods=['GET', 'POST', 'DELETE'])
def edit_variable(category, name):
    return variables.views.edit_variable(request, category, name)
'''


@app.route('/api/v1.0/variables', methods=['GET', 'POST'])
def api_variables():
    return jsonify(variables.api.variables(request))


@app.route('/api/v1.0/variables/categories', methods=['GET'])
def api_variables_category():
    return jsonify(variables.api.variables_category(request))


@app.route('/api/v1.0/variables/categories/<category>', methods=['GET'])
def api_variables_filter_by_category(category):
    return jsonify(variables.api.variables_filter_by_category(request, category))


@app.route('/api/v1.0/variables/categories/<category>/<name>', methods=['GET', 'PUT', 'DELETE'])
def api_variables_name(category, name):
    return jsonify(variables.api.api_variables_name(request, category, name))

###################
###################
#  PMACCT_DATA  ###
###################
###################


@app.route('/api/v1.0/pmacct/dates', methods=['GET'])
def pmacct_data_get_dates():
    return jsonify(pmacct_data.api.get_dates(request))


@app.route('/api/v1.0/pmacct/flows', methods=['GET'])
def pmacct_data_get_flows():
    return jsonify(pmacct_data.api.get_flows(request))


@app.route('/api/v1.0/pmacct/bgp_prefixes', methods=['GET'])
def pmacct_get_bgp_prefixes():
    return jsonify(pmacct_data.api.get_bgp_prefixes(request, app.config['BGP_FOLDER']))


if __name__ == '__main__':
    app.run(app.config['BIND_IP'], app.config['PORT'])
