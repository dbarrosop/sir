=============
Configuration
=============

Configuring the SDN Internet Router is very easy. There are a few global parameters and then there are some that are backend/plugin specific. For those, check the backend/plugin documentation. Below there is a configuration example::

    history: 72 # How many days to consider for the best prefixes
    max_routes: 30000 # Maximum routes allowed
    packet_sampling: 10000 # Packet sampling configured on the flow agent

    # Logging options
    logging_level: DEBUG
    log_to_syslog: False
    syslog_server_ip: 127.0.0.1
    syslog_server_port: 514
    log_to_stderr: True

    # Where pmacct stores the BGP feed
    pmacct_bgp_folder: '/pmacct_data/output/bgp'

    # Backend to use and backend configuration
    backend: 'sqlite.SQLite'
    backend_options:
      sqlite_file: '/pmacct_data/output/flows/pmacct.db' # Path to the SQLite database
      retention: 7 # Days to hold old data.

    # Options for the simulator
    simulate:
      date_format: '%Y-%m-%d %H:%M:%S'
      start_date: '2012-12-12 00:00:00'
      end_date: '2015-12-20 00:00:00'

    # List of plugins to run
    plugins:
      - 'statistics.RouteStatistics'
      - 'statistics.OffloadedBytes'
      - 'bird.Bird'

    ###########################################################################
    # Configuration below is specific to the plugins I am using. Check their
    # documentation for more info.
    ###########################################################################

    # Used by plugin statistics.RouteStatistics. See more details on the plugin documentation.
    RouteStatistics:
      db_table: 'route_statistics'
      png_file: '/Users/dbarroso/Documents/workspace/pmacct_data/route_statistics.png'
      plot_days: 2

    # Used by plugin statistics.OffloadedBytes. See more details on the plugin documentation.
    OffloadedBytes:
      db_table: 'offloaded_bytes'
      png_file: '/Users/dbarroso/Documents/workspace/pmacct_data/offloaded_bytes.png'
      plot_days: 2

    # Used by plugin bird.Bird. See more details on the plugin documentation.
    Bird:
      policy_file: '/Users/dbarroso/Documents/workspace/pmacct_data/allow_prefixes.bird'
      reload_bird: False
