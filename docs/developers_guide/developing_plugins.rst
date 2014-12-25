******************
Developing plugins
******************

Developing plugins is very easy. What you have to do is to write a class that inherits from *plugins.base.PrefixPlugin*, configure a few class constants and overwrite the method **run**::

    from base import PrefixPlugin

    class FooPlugin(PrefixPlugin):
        skip_simulation = False
        run_once_during_simulations = True

        def run(self):
            print "foo"

Class Constants
===============

When you create your own plugin you have to set two constants that will define when your plugin will be triggered:

    - **skip_simulation**: If set to *True* the plugin will not be executed in *simulations*.
    - **run_once_during_simulations**: If set to *True*, when running in *simulations*, the plugin will be called on the last iteration of the simulation. If set to *False*, it will be called on every iteration.

Variables
=========

When you plugin is called it will contain the following variables:

    - **conf**: A dictionary containing all the parameters set on the configuration file.
    - **backend** An instance of the backend. Useful to store and retrieve data from the backend.
    - **data_file**: Filename of the pmacct file we are processing
    - **raw_pt**: A PrefixTable containing all prefixes that have been processed
    - **new_pt**: A PrefixTable containing only the prefixes that have passed our criteria
    - **prev_pt**: A PrefixTable containing the prefixes that we had until now.
    - **bgp_table**: A dictionary containing the BGP feed that pmacct is getting.
    - **time**: Time of this run
    - **simulation**: True if we are running a simulation.
    - **last_run**: True if it is the last iteration of the simulation or if it's not a simulation.

Configuration Options
=====================

If you need to add configuration variables for your backend like connection string, username, password,
or others, you can specify them in the configuration file inside a dictionary. For example::

    RouteStatistics:
      db_table: 'route_statistics'
      png_file: '/Users/dbarroso/Documents/workspace/pmacct_data/route_statistics.png'
      plot_days: 2

You will be able to access those variables as 'self.conf[variable_name]'. For example::

    >>> print self.conf['RouteStatistics']['plot_days']
    2

Backend Methods
===============

There are two useful methods that backends have to provide that are useful for writing plugins. These are:

   * :py:meth:`bgp_controller.backend.base.Backend.save_dict`
   * :py:meth:`bgp_controller.backend.base.Backend.get_data_from_table`

Check the :py:class:`~bgp_controller.backend.base.Backend` documentation for more info on how to use those methods.

Documenting the Plugin
======================

For convenience we will document every plugin using the class docstring. We will follow the following format for standarization::

    """
    Name:
        Name of the plugin
    Author:
        Author's Name <Author's email>
    Description:
        Description of what the module does
    Requires:
        A list containing which variables are required.
    Configuration:
        A list containing which configuration parameters are required and why.
    """

Example
=======

To wrap up, check the following plugin as an example::

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
            saved on a CSV file with the following format::

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


