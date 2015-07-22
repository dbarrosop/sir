========
Scenario
========

You can deploy the SDN Internet Router in many ways. Below you can find the simplest deployment where the SDN Internet Router might be useful. We will also use this example to show how to deploy the BGP Controller.

.. image:: ../img/how_to_scenario.png
   :alt: Network Diagram

Our Internet Router is connected to:

 - **Transit provider** - Our transit provider will send the default route only.
 - **Peer** - Peers will send a bunch of prefixes belonging to them. For the sake of simplicity we have only one peer and it´s on the same network as the Transit Provider.
 - **DC** - From the DC we will get the network where our servers are located.

The Internet Router will be configured with the following default configuration:

 - Readvertise the networks coming from the **DC** to our **Transit Provider** and our **peers**.
 - Readvertise the default route to our **DC**.
 - Accept the default route coming from the **Transit provider**
 - Reject everything incoming from our **peers**.

This means that the Internet Router by default will:

 - Get traffic inbound from the **Transit Provider** and our **peers** directed towards our **DC**.
 - Send traffic outbound towards our **Transit Provider** only.

Using a router running *bird* the configuration will be as follows (when installing *bird* make sure you are using a recent version of the software)::

    # This file includes the allow_prefixes() method, which will
    # decide which prefixes to install on the routing table.
    include "/etc/bird/allow_prefixes.bird";

    router id 10.0.0.10;
    log syslog all;
    debug protocols all;

    listen bgp address 10.0.0.10 port 179;
    listen bgp address 10.0.1.10 port 179;

    # protocol kernel will control which routes go from the RIB to the FIB
    protocol kernel {
        export filter {
            # We accept the routes coming from our Transit Provider
            if from = 10.0.0.1 then accept;
            # We also accept everything coming from our DC
            if from = 10.0.1.11 then accept;
            # This method is what the BGP controller will update later
            if allow_prefixes() then accept;
            # The rest is rejected.
            reject;
        };
    }

    protocol device {
        scan time 10;
        primary 10.0.0.0/24;
        primary 10.0.1.0/24;
    }

    # Transit Provider
    protocol bgp {
        local as 65010;
        neighbor 10.0.0.1 as 65001;

        export filter {
            # We only send the route coming from the DC
            if from = 10.0.1.11 then accept;
            reject;
        };
    }

    # Peer
    protocol bgp {
        local as 65010;
        neighbor 10.0.0.2 as 65002;

        export filter {
            # We only send the route coming from the DC
            if from = 10.0.1.11 then accept;
            reject;
        };
    }

    # DC
    protocol bgp {
        local as 65010;
        neighbor 10.0.1.11 as 65011;

        export filter {
            # We only want to send the default route to the DC
            if net = 0.0.0.0/0 then accept;
            reject;
        };
    }

In addition you will have to create the file */etc/bird/allow_prefixes.bird* with the following content::

    function allow_prefixes()
    {
      return net ~ [
        # Dummy prefix that you will surely not have in your RIB.
        # The reason for this is that the list cannot be empty.
        1.2.3.4/32
      ];
    }

Let´s see if this is working::

    # We start the service
    $ sudo service bird start
    [ ok ] Starting BIRD Internet Routing Daemon (IPv4): bird.

    # We connect to bird
    $ sudo birdc

    # Routes from the Transit Provider
    bird> show route protocol bgp1
    0.0.0.0/0          via 10.0.0.1 on eth1 [bgp1 10:36] * (100) [AS65001i]

    # Routes from the Peer
    bird> show route protocol bgp2
    188.3.176.0/21     via 10.0.0.2 on eth1 [bgp2 10:36] * (100) [AS65002i]
    194.3.206.0/24     via 10.0.0.2 on eth1 [bgp2 10:36] * (100) [AS65002i]
    212.5.192.0/19     via 10.0.0.2 on eth1 [bgp2 10:36] * (100) [AS65002i]
    194.8.226.0/23     via 10.0.0.2 on eth1 [bgp2 10:36] * (100) [AS65002i]
    ...

    # Routes from the DC
    bird> show route protocol bgp3
    192.168.0.0/24     via 10.0.1.11 on eth2 [bgp3 10:36] * (100) [AS65011i]

    # Routes to the Transit Provider and the Peer
    bird> show route export bgp1
    192.168.0.0/24     via 10.0.1.11 on eth2 [bgp3 10:36] * (100) [AS65011i]
    bird> show route export bgp2
    192.168.0.0/24     via 10.0.1.11 on eth2 [bgp3 10:36] * (100) [AS65011i]

    # Routes to the DC
    bird> show route export bgp3
    0.0.0.0/0          via 10.0.0.1 on eth1 [bgp1 10:36] * (100) [AS65001i]

    # Routes installed on the FIB
    bird> show route export kernel1
    0.0.0.0/0          via 10.0.0.1 on eth1 [bgp1 10:36] * (100) [AS65001i]
    192.168.0.0/24     via 10.0.1.11 on eth2 [bgp3 10:36] * (100) [AS65011i]

As you can see we are doing exactly what we described before. So far, the routes coming from our **peer** are just being ignored. We are not installing them on the FIB. The BGP Controller will override this behavior later by modifying the contents of the file */etc/bird/allow_prefixes.bird*.
