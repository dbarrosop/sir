=================
Operational Modes
=================

You can run the SDN Internet router in two modes:

    - **run** - This is the normal mode of operation.
    - **simulate** - This mode allows you to simulate how the SDN Internet router would behave during a period of time.

It is important to note that each operational mode will affect how plugins work. Some plugins will not run at all in *"simulate"* mode and some others will run a particular code on each iteration of the simulation and another code on the last iteration of the simulation. Check the plugins documentation for more info.

--------
Run mode
--------

It will get the best prefixes from the backend within the time range *"from now to now-conf['history']"*. To run sir on this mode execute::

    env python sir.py run -c etc/config.yaml

-------------
Simulate mode
-------------

This mode allows you to test how the SDN Internet Router would work during a period of time. The only requisite is that you must have data for that specific period. For example, if I want to test how my SDN Internet Router would work during a period of time I could add the following configuration options::

    simulate:
      date_format: '%Y-%m-%d %H:%M:%S'
      start_date: '2014-12-18 00:00:00'
      end_date: '2014-12-20 00:00:00'

That would instruct sir to run the simulator within the period of time 2014-12-18 to 2014-12-20. To run the simulator execute::

    env python sir.py simulate -c etc/config.yaml