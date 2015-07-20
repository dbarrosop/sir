#TODO Variables primary key name and category and modify calls
#TODO Browse variables
#TODO metrics
#TODO Improve building the response of the API and documentation
#TODO Python API
#TODO Build first app
#TODO Expose raw BGP
#TODO Expose raw flows
#TODO Catch errors in API


from helpers.SQLite3Helper import SQLite3Helper

from helpers import analytics
from helpers import api
from helpers import basic

from flask import Flask, request, g, jsonify

import time

app = Flask(__name__)
app.config.from_object('settings')

###################
###################
####  BASIC  ######
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
    return basic.start_page(g, request)

###################
###################
###  ANALYTICS  ###
###################
###################


@app.route('/analytics', strict_slashes=False)
def analytics_help():
    return analytics.start_page(g, request)


@app.route('/analytics/offloaded_traffic', methods=['GET', 'POST'])
def analytics_offloaded_traffic():
    return analytics.offloaded_traffic(g, request)


@app.route('/analytics/aggregate_per_as', methods=['GET', 'POST'])
def analytics_aggregate_per_as():
    return analytics.aggregate(g, request, 'as')


@app.route('/analytics/aggregate_per_prefix', methods=['GET', 'POST'])
def analytics_aggregate_per_prefix():
    return analytics.aggregate(g, request, 'prefix')


@app.route('/analytics/simulate', methods=['GET', 'POST'])
def analytics_simulate():
    return analytics.simulate(g, request)

###################
###################
######  API  ######
###################
###################


@app.route('/api/v1.0', strict_slashes=False)
def api_help():
    return api.start_page(g, request)


@app.route('/api/v1.0/analytics/top_prefixes', methods=['GET'])
def api_top_prefixes():
    return jsonify(api.top_prefixes(g, request))


@app.route('/api/v1.0/analytics/top_asns', methods=['GET'])
def api_top_asns():
    return jsonify(api.top_asns(g, request))


@app.route('/api/v1.0/variables', methods=['GET', 'POST'])
def api_variables():
    return jsonify(api.variables(g, request))


@app.route('/api/v1.0/variables/categories', methods=['GET'])
def api_variables_category():
    return jsonify(api.variables_category(g, request))


@app.route('/api/v1.0/variables/categories/<category>', methods=['GET'])
def api_variables_filter_by_category(category):
    return jsonify(api.variables_filter_by_category(g, request, category))


@app.route('/api/v1.0/variables/categories/<category>/<name>', methods=['GET', 'PUT', 'DELETE'])
def api_variables_name(category, name):
    return jsonify(api.api_variables_name(g, request, category, name))


if __name__ == '__main__':
    app.run()
