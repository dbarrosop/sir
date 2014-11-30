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
    - **run_once_during_simulations**: If set to *True*, when running in *simulations*, the plugin will be called on the last iteration of the simulation. If set to *False, it will be called on every iteration.

Variables
=========

When you plugin is called it will contain the following variables:

    - **conf**: A dictionary containing all the parameters set on the configuration file.
    - **data_file**: Filename of the pmacct file we are processing
    - **raw_pt**: A PrefixTable containing all prefixes that have been processed
    - **new_pt**: A PrefixTable containing only the prefixes that have passed our criteria
    - **prev_pt**: A PrefixTable containing the prefixes that we had until now.
    - **bgp_table**: A dictionary containing the BGP feed that pmacct is getting.
    - **time**: Time of this run
    - **simulation**: True if we are running a simulation.
    - **last_run**: True if it is the last iteration of the simulation or if it's not a simulation.

Documenting the Plugin
======================

For convenience we will document every plugin using the class docstring. We will follow the following format for standarization::

    """
    Name:
        Name of the plugin
    Author:
        Author Name <Author email>
    Description:
        Description of what the module does
    Requires:
        A list containing with variables are required.
    Configuration:
        A list containing with configuration parameters are required and why.
    """

Example
=======

To wrap up, check the following plugin as an example::

    from base import PrefixPlugin
    import os
    from shutil import copyfile


    class RouteStatistics(PrefixPlugin):
        """
        Name:
            RouteStatistics
        Author:
            David Barroso <dbarroso@spotify.com>
        Description:
            Keeps historical data of which prefixes are added, kept, removed, etc. on every run. The data is
            saved on a CSV file with the following format:
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

        # We want to run the plugin during simulations
        skip_simulation = False
        # We want to run it on every iteration
        run_once_during_simulations = False

        def process_data(self):
            # We can add our own methods for clarity and reusability

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
            # We can add our own methods for clarity and reusability
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
            # The run method is triggered by the BGP controller
            self.process_data()

            # Only plot the graph if it's the last run
            if self.last_run:
                self.plot()
