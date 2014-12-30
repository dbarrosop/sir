===============
Configuring sir
===============

First step is to clone the GIT repository and install the requirements::

    $ cd /
    $ git clone git@github.com:dbarrosop/sir.git
    $ cd sir
    $ pip install -r requirements.txt

Then you will need a configuration file with a content similar to the following::

    history: 72
    max_routes: 30000 # Maximum routes allowed
    packet_sampling: 10000 # Packet sampling configured on the flow agent

    logging_level: DEBUG
    log_to_syslog: False
    syslog_server_ip: 127.0.0.1
    syslog_server_port: 514
    log_to_stderr: True

    # Where pmacct stores the BGP feed
    pmacct_bgp_folder: '/bgp_controller/bgp'

    backend: 'sqlite.SQLite'
    backend_options:
      sqlite_file: '/bgp_controller/bgpc.db' # Path to the SQLite database
      retention: 7 # Days to hold old data.

    simulate:
      date_format: '%Y-%m-%d %H:%M:%S'
      start_date: '2014-12-18 00:00:00'
      end_date: '2014-12-20 00:00:00'

    # List of plugins to run
    plugins:
      - 'statistics.RouteStatistics'
      - 'statistics.OffloadedBytes'
      - 'bird.Bird'

    # Used by plugin statistics.RouteStatistics. See more details on the plugin documentation.
    RouteStatistics:
      db_table: 'route_statistics'
      png_file: '/bgp_controller/route_statistics.png'
      plot_days: 1

    # Used by plugin statistics.OffloadedBytes. See more details on the plugin documentation.
    OffloadedBytes:
      db_table: 'offloaded_bytes'
      png_file: '/bgp_controller/offloaded_bytes.png'
      plot_days: 1

    # Used by plugin bird.Bird. See more details on the plugin documentation.
    Bird:
      policy_file: '/etc/bird/allow_prefixes.bird'
      reload_bird: True

Where you keep the configuration file is up to you, I will use **/etc/sir-conf.yaml**. Now, we have to adapt the backend::

    # sir
    $ sqlite3 /bgp_controller/bgpc.db < /sir/sql/sir.sql

    # Needed for the plugins I am using. Check the documentation of the plugins for more information.
    $ sqlite3 /bgp_controller/bgpc.db < /sir/sql/plugins/offloaded_bytes.sql
    $ sqlite3 /bgp_controller/bgpc.db < /sir/sql/plugins/route_statistics.sql

