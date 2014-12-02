from base import PrefixPlugin

import pandas as pd
import os
import matplotlib

matplotlib.use('Agg')

# TODO make sure it runs in 'run' mode
# TODO select how many hours you want to graph

class RouteStatistics(PrefixPlugin):
    """
    Name:
        RouteStatistics
    Author:
        David Barroso <dbarroso@spotify.com>
    Description:
        Keeps historical data of which prefixes are added, kept, removed, etc. on every run. The data is
        saved on a CSV file with the following format::

            Time,Total,Kept,Added,Removed,Expired

        In addition it will generate a graph for better visualization.
    Requires:
        - prev_pt
        - new_pt
        - time
    Configuration:
        - route_statistics_file: Where to store the data
        - route_statistics_png_file: Where to save the graph
        - max_routes: Maximum routes allowed (for decoration)
        - min_bytes: Min bytes necessary to consider a prefix eligible (for decoration)
        - max_age: Maximum age a route can be present without any traffic (for decoration)
    """

    skip_simulation = False
    run_once_during_simulations = False

    def process_data(self):
        total = len(self.new_pt)
        kept = len(self.new_pt.common_prefixes(self.prev_pt))
        removed = len(self.prev_pt.missing_prefixes(self.new_pt)) - self.new_pt.expired_prefixes
        added = len(self.new_pt.missing_prefixes(self.prev_pt))

        if os.path.exists(self.conf['route_statistics_file']):
            add_headers = False
        else:
            add_headers = True

        with open(self.conf['route_statistics_file'], "a") as f:
            if add_headers:
                line = 'Time,Total,Kept,Added,Removed,Expired\n'
                f.write(line)
            line = '%s, %s, %s, %s, %s, %s\n' % (self.time, total, kept, added, removed, self.new_pt.expired_prefixes)
            f.write(line)
            f.close()

    def plot(self):
        pd.set_option('display.mpl_style', 'default')
        data = pd.read_csv(self.conf['route_statistics_file'])
        plot = data.plot(
            x='Time',
            figsize = (9,9),
            grid=True,
            title='Route Statistics, max_routes: %s, min_bytes: %s, max_age: %s' %
                  (self.conf['max_routes'], self.conf['min_bytes'], self.conf['max_age']),
            legend=True,
        )
        fig = plot.get_figure()
        fig.savefig(self.conf['route_statistics_png_file'])

    def run(self):
        self.process_data()

        if self.last_run:
            self.plot()


class OffloadedBytes(PrefixPlugin):
    """
    Name:
        OffloadedBytes
    Author:
        David Barroso <dbarroso@spotify.com>
    Description:
        Keeps historical data of how much data is send and how much is offloaded. We consider that data is
        offloaded when a prefix in raw_pt was present in prev_pt. The data saved on the CSV file has the
        following format::

            Time,Total,Offloaded,%

        In addition it will generate a graph for better visualization.
    Requires:
        - raw_pt
        - prev_pt
        - time
    Configuration:
        - draw_offloaded_bytes_file: Where to store the data
        - draw_offloaded_bytes_png_file: Where to save the graph
        - max_routes: Maximum routes allowed (for decoration)
        - min_bytes: Min bytes necessary to consider a prefix eligible (for decoration)
        - max_age: Maximum age a route can be present without any traffic (for decoration)
    """

    skip_simulation = False
    run_once_during_simulations = False

    def plot(self):
        pd.set_option('display.mpl_style', 'default')
        data = pd.read_csv(self.conf['draw_offloaded_bytes_file'])
        plot = data.plot(
            x='Time',
            secondary_y=['%'],
            figsize = (9,9),
            grid=True,
            title='Data Offloaded, max_routes: %s, min_bytes: %s, max_age: %s' %
                  (self.conf['max_routes'], self.conf['min_bytes'], self.conf['max_age']),
            legend=True,
        )
        fig = plot.get_figure()
        fig.savefig(self.conf['draw_offloaded_bytes_png_file'])

    def process(self):
        ol_bytes = sum(p.get_bytes() for p in self.raw_pt if self.prev_pt.prefix_present(p))
        total_bytes = self.raw_pt.get_total_bytes()
        percentage = ol_bytes*100/total_bytes

        if os.path.exists(self.conf['draw_offloaded_bytes_file']):
            add_headers = False
        else:
            add_headers = True

        with open(self.conf['draw_offloaded_bytes_file'], "a") as f:
            if add_headers:
                line = 'Time,Total,Offloaded,%\n'
                f.write(line)
            line = '%s, %s, %s, %s\n' % (self.time, total_bytes, ol_bytes, percentage)
            f.write(line)
            f.close()

    def run(self):
        self.process()

        if self.last_run:
            self.plot()
