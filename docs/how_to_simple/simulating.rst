==============
Simulating sir
==============

Before running sir in production you might want just to let pmacct collect data for a coupe of days and then run sir in simulation mode. That will let you test how the system is going to behave. You can easily do that by doing some small changes on the configuration (showing only relevant configuration)::

    # We can try different parameters
    history: 72
    max_routes: 30000 # Maximum routes allowed
    packet_sampling: 10000 # Packet sampling configured on the flow agent

    # We log to stderr instead to syslog
    logging_level: DEBUG
    log_to_syslog: False
    syslog_server_ip: 127.0.0.1
    syslog_server_port: 514
    log_to_stderr: True

    pmacct_bgp_folder: '/bgp_controller/bgp'

    backend: 'sqlite.SQLite'
    backend_options:
      sqlite_file: '/bgp_controller/bgpc.db' # Path to the SQLite database
      retention: 7 # Days to hold old data.

    # Simulation period
    simulate:
      date_format: '%Y-%m-%d %H:%M:%S'
      start_date: '2014-12-18 00:00:00'
      end_date: '2014-12-20 00:00:00'

    plugins:
      - 'statistics.RouteStatistics'
      - 'statistics.OffloadedBytes'
      - 'bird.Bird'

    RouteStatistics:
      db_table: 'route_statistics'
      png_file: '/bgp_controller/route_statistics.png'
      plot_days: 1

    OffloadedBytes:
      db_table: 'offloaded_bytes'
      png_file: '/bgp_controller/offloaded_bytes.png'
      plot_days: 1

    # We don't want bird to reload the process
    Bird:
      policy_file: '/etc/bird/allow_prefixes.bird'
      reload_bird: False


You can try different parameters to see how it behaves. The key points is instruct the bird plugin to not reload the configuration and to setup the proper dates for the simulation. Now we can try to run the simulation::

    $ env python sir.py simulate -c /etc/sir-conf.yaml
    INFO:sir:action=SIMULATE
    INFO:sir:action=OPEN_BACKEND backend=SQLITE file=/bgp_controller/bgpc.db
    DEBUG:sir:action=GET_AVAILABLE_DATES_IN_RANGE start_time=2014-12-18 00:00:00 end_time=2014-12-20 00:00:00
    INFO:sir:action=PROCESS_PREFIX start_date=2014-12-17 23:00:01 end_date=2014-12-18 11:00:01
    DEBUG:sir:action=GET_PREVIOUS_PREFIXES start_time=2014-12-17 23:00:01 end_time=2014-12-18 11:00:01
    DEBUG:sir:action=GET_BEST_PREFIXES start_time=2014-12-17 23:00:01 end_time=2014-12-18 11:00:01
    DEBUG:sir:action=SAVE_PREFIX_TABLE date=2014-12-18 11:00:01
    DEBUG:sir:action=GET_RAW_PREFIXES start_time=2014-12-17 23:00:01 end_time=2014-12-18 11:00:01
    INFO:sir:action=EXECUTE_PLUGIN plugin=statistics.RouteStatistics
    DEBUG:sir:action=SAVE_DICT db_table=route_statistics
    INFO:sir:action=EXECUTE_PLUGIN plugin=statistics.OffloadedBytes
    DEBUG:sir:action=SAVE_DICT db_table=offloaded_bytes
    INFO:sir:action=EXECUTE_PLUGIN plugin=bird.Bird
    ...
    INFO:sir:action=PROCESS_PREFIX start_date=2014-12-16 23:00:01 end_date=2014-12-19 23:00:01
    DEBUG:sir:action=GET_PREVIOUS_PREFIXES start_time=2014-12-16 23:00:01 end_time=2014-12-19 23:00:01
    DEBUG:sir:action=GET_BEST_PREFIXES start_time=2014-12-16 23:00:01 end_time=2014-12-19 23:00:01
    DEBUG:sir:action=SAVE_PREFIX_TABLE date=2014-12-19 23:00:01
    DEBUG:sir:action=GET_RAW_PREFIXES start_time=2014-12-16 23:00:01 end_time=2014-12-19 23:00:01
    INFO:sir:action=EXECUTE_PLUGIN plugin=statistics.RouteStatistics
    DEBUG:sir:action=SAVE_DICT db_table=route_statistics
    INFO:sir:action=EXECUTE_PLUGIN plugin=statistics.OffloadedBytes
    DEBUG:sir:action=SAVE_DICT db_table=offloaded_bytes
    INFO:sir:action=EXECUTE_PLUGIN plugin=bird.Bird
    INFO:sir:action=CLOSE_BACKEND backend=SQLITE file=/bgp_controller/bgpc.db

If everything worked as expected and you run the same plugins as I did you should have:

 * The file *'/etc/bird/allow_prefixes.bird'* with content::

    $ cat  /etc/bird/allow_prefixes.bird
    function allow_prefixes() {
      return net ~ [
        87.238.168.0/21,
        186.182.128.0/18,
        87.99.0.0/18,
        212.15.224.0/20,
        92.255.216.0/22,
        185.25.216.0/22,
        193.37.237.0/24,
        46.21.216.0/21,
        ... (output truncated)
        212.233.136.0/24,
        181.199.192.0/19,
        195.3.173.0/24,
        213.180.64.0/19,
        91.209.141.0/24,
        145.88.0.0/15,
        87.234.0.0/16,
        105.158.48.0/21
      ];
    }

 * Similar graphs to the ones below on the folder *'/bgp_controller/'*

    * Offloaded Bytes

        .. image:: ../img/offloaded_bytes.png
            :alt: Offloaded Bytes
    * Route Statistics

        .. image:: ../img/route_statistics.png
            :alt: Route Statistics

Hopefully, this will be enough hints on how to use the BGP Controller to get the most of your network.