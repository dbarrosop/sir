from helpers.SQLite3Helper import SQLite3Helper
from helpers import analytics

from flask import Flask, request, g, render_template

app = Flask(__name__)
app.config.from_object('settings')

@app.before_request
def before_request():
    g.db = SQLite3Helper(app.config['DATABASE'])
    g.db.connect()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/view', strict_slashes=False)
def view_help():
    return render_template('view/help.html')

@app.route('/view/aggregate_per_as', methods=['GET', 'POST'])
def view_aggregate_per_as():
    db = getattr(g, 'db', None)
    context = analytics.aggregate(db, request, 'as')
    return render_template('view/analytics_aggregate.html', **context)

@app.route('/view/aggregate_per_prefix', methods=['GET', 'POST'])
def view_aggregate_per_prefix():
    db = getattr(g, 'db', None)
    context = analytics.aggregate(db, request, 'prefix')
    return render_template('view/analytics_aggregate.html', **context)

@app.route('/view/offloaded_traffic', methods=['GET', 'POST'])
def view_offloaded_traffic():
    db = getattr(g, 'db', None)
    context = analytics.offloaded_traffic(db, request)
    return render_template('view/offloaded_traffic.html', **context)

@app.route('/view/simulate', methods=['GET', 'POST'])
def view_simulate():
    db = getattr(g, 'db', None)
    context = analytics.view_simulate(db, request)
    return render_template('view/simulate.html', **context)

if __name__ == '__main__':
    app.run()
