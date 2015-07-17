from helpers.SQLite3Helper import SQLite3Helper

from helpers import views
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
####  VIEWS  ######
###################
###################


@app.route('/views', strict_slashes=False)
def view_help():
    return views.start_page(g, request)


@app.route('/views/offloaded_traffic', methods=['GET', 'POST'])
def view_offloaded_traffic():
    return views.offloaded_traffic(g, request)


@app.route('/views/aggregate_per_as', methods=['GET', 'POST'])
def view_aggregate_per_as():
    return views.aggregate(g, request, 'as')


@app.route('/views/aggregate_per_prefix', methods=['GET', 'POST'])
def view_aggregate_per_prefix():
    return views.aggregate(g, request, 'prefix')


@app.route('/views/simulate', methods=['GET', 'POST'])
def view_simulate():
    return views.simulate(g, request)

###################
###################
######  API  ######
###################
###################


@app.route('/api/v1.0', strict_slashes=False)
def api_help():
    return api.start_page(g, request)


@app.route('/api/v1.0/top_prefixes', methods=['GET'])
def api_top_prefixes():
    return jsonify(api.top_prefixes(g, request))


@app.route('/api/v1.0/top_asns', methods=['GET'])
def api_top_asns():
    return jsonify(api.top_asns(g, request))


if __name__ == '__main__':
    app.run()
