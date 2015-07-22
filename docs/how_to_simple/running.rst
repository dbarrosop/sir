===========
Running sir
===========

Now it's time to run it and see if it works::

    # We check the routing table first
    $ sudo ip route | grep bird
    192.168.0.0/24 via 10.0.1.11 dev eth2  proto bird

    # We run the controller
    $ python /sir/sir.py run -c /etc/sir-conf.yaml
    BIRD 1.4.5 ready.
    Reading configuration from /etc/bird/bird.conf
    Reconfigured

If we don't get any error we check the routing table again and the content of the directory *'/bgp_controller/'*::

    $ ip route | grep bird
    130.239.0.0/16 via 10.0.0.2 dev eth1  proto bird
    185.31.17.0/24 via 10.0.0.2 dev eth1  proto bird
    192.30.252.0/24 via 10.0.0.2 dev eth1  proto bird
    192.168.0.0/24 via 10.0.1.11 dev eth2  proto bird
    195.20.224.0/19 via 10.0.0.2 dev eth1  proto bird
    $ ls /spotify/sir_data/
    latest_data.csv      offloaded_bytes.png   route_statistics.png
    bgp  bgpc.db

Now you have to make sure you run the controller every hour after pmacct has saved the data on disc. To do that you can add a cron task, create the file **/etc/cron.d/sir** with the content::

    5 * * * *   root    /usr/bin/env python /sir/sir.py run -c /etc/sir-conf.yaml

