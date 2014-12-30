from base import PrefixPlugin

import pandas as pd
import matplotlib

matplotlib.use('Agg')

class RouteStatistics(PrefixPlugin):
    """
    Name:
        RouteStatistics
    Author:
        David Barroso <dbarroso@spotify.com>
    Description:
        Keeps historical data of which prefixes are added, kept, removed, etc. on every run. The data is
        saved in the backend with the following format::

            Time,Total,Kept,Added,Removed,Expired

        In addition it will generate a graph for better visualization.
    Requires:
        - prev_pt
        - new_pt
        - time
    Configuration:
        - db_table: Where to store/retrieve the data in the backend
        - png_file: Where to save the graph
        - plot_days: Days to plot
    Example:
        Configuration example::

            RouteStatistics:
              db_table: 'route_statistics'
              png_file: '/Users/dbarroso/Documents/workspace/pmacct_data/route_statistics.png'
              plot_days: 2

        You can adapt the backend database to use this plugin by using the sql script provided in the folder
        *'/sql/plugins/route_statistics.sql'*
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

        for row in table[1:]:
            raw_data.append(
                {
                    table[0][0]: row[0],
                    table[0][1]: row[1],
                    table[0][2]: row[2],
                    table[0][3]: row[3],
                    table[0][4]: row[4],
                }
            )
        time_frame = self.conf['RouteStatistics']['plot_days']*24
        data = pd.DataFrame(raw_data)[-time_frame:]
        plot = data.plot(
            x='time',
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
        offloaded when a prefix in raw_pt was present in prev_pt. The data saved on the backend has the
        following format::

            Time,Total,Offloaded,%

        In addition it will generate a graph for better visualization.
    Requires:
        - raw_pt
        - prev_pt
        - time
    Configuration:
        - db_table: Where to store/retrieve the data in the backend
        - png_file: Where to save the graph
        - plot_days: Days to plot
    Example:
        Configuration example::

            OffloadedBytes:
              db_table: 'offloaded_bytes'
              png_file: '/Users/dbarroso/Documents/workspace/pmacct_data/offloaded_bytes.png'
              plot_days: 2

        You can adapt the backend database to use this plugin by using the sql script provided in the folder
        *'/sql/plugins/offloaded_bytes.sql'*

    """

    skip_simulation = False
    run_once_during_simulations = False

    def plot(self):
        pd.set_option('display.mpl_style', 'default')

        table = self.backend.get_data_from_table(self.conf['OffloadedBytes']['db_table'])

        raw_data = list()

        for row in table[1:]:
            raw_data.append(
                {
                    table[0][0]: row[0],
                    table[0][1]: row[1],
                    table[0][2]: float(row[2]),
                    table[0][3]: row[3],
                }
            )
        time_frame = self.conf['OffloadedBytes']['plot_days']*24
        data = pd.DataFrame(raw_data)[-time_frame:]

        plot = data.plot(
            x='time',
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
