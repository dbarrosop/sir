from base import PrefixPlugin

import pandas as pd
import os
import matplotlib

matplotlib.use('Agg')

# TODO make sure it runs in 'run' mode
# FIXME Update documentation

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
        data = dict()
        data['time'] = self.time.strftime('%Y-%m-%d %H:%M:%S')
        data['total'] = len(self.new_pt)
        data['kept'] = len(self.new_pt.common_prefixes(self.prev_pt))
        data['removed'] = len(self.prev_pt.missing_prefixes(self.new_pt)) - self.new_pt.expired_prefixes
        data['added'] = len(self.new_pt.missing_prefixes(self.prev_pt))

        self.backend.save_dict(data, self.conf['RouteStatistics']['db_table'])

    def plot(self):
        pd.set_option('display.mpl_style', 'default')
        table = self.backend.get_data_from_table(self.conf['RouteStatistics']['db_table'])

        raw_data = list()

        for row in table:
            raw_data.append(
                {
                    'date': row[0],
                    'total': row[1],
                    'kept': row[2],
                    'removed': row[3],
                    'added': row[4],
                }
            )
        time_frame = self.conf['RouteStatistics']['plot_days']*24
        data = pd.DataFrame(raw_data)[-time_frame:]
        plot = data.plot(
            x='date',
            figsize = (9,9),
            grid=True,
            title='Route Statistics, max_routes: %s, history: %s' %
                  (self.conf['max_routes'], self.conf['history']),
            legend=True,
        )
        fig = plot.get_figure()
        fig.savefig(self.conf['RouteStatistics']['png_file'])

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

        table = self.backend.get_data_from_table(self.conf['OffloadedBytes']['db_table'])

        raw_data = list()

        for row in table:
            raw_data.append(
                {
                    'date': row[0],
                    'total_bytes': row[1],
                    'offloaded': float(row[2]),
                    'percentage': row[3],
                }
            )
        time_frame = self.conf['OffloadedBytes']['plot_days']*24
        data = pd.DataFrame(raw_data)[-time_frame:]

        plot = data.plot(
            x='date',
            secondary_y=['percentage'],
            figsize = (9,9),
            grid=True,
            title='Data Offloaded, max_routes: %s, history: %s' %
                  (self.conf['max_routes'], self.conf['history']),
            legend=True,
        )
        fig = plot.get_figure()
        fig.savefig(self.conf['OffloadedBytes']['png_file'])

    def process(self):
        data = dict()
        data['time'] = self.time.strftime('%Y-%m-%d %H:%M:%S')
        data['total_bytes'] = self.raw_pt.get_total_bytes()
        data['offloaded'] = sum(p.get_bytes() for p in self.raw_pt if self.prev_pt.prefix_present(p))

        data['percentage'] = float(data['offloaded'])*100/float(data['total_bytes'])

        self.backend.save_dict(data, self.conf['OffloadedBytes']['db_table'])

    def run(self):
        self.process()

        if self.last_run:
            self.plot()
