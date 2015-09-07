=============
fib_optimizer
=============

One of the main use cases of SIR is using a switch for peering purposes. Traditionally routers has been used for that
purpose as switches had limited routing table. However, with SIR and the fib_optimizer app you can use instead a switch
and bring down costs. For more information about this use case go to the section :ref:`A commodity switch as a Peering Router`.

For more details about the fib_optimizer go to the github repo where the
`fib_optimizer <https://github.com/dbarrosop/sir_apps/tree/master/fib_optimizer>`_ lives. For instructions on how to
easily deploy it within EOS keep reading.

.. warning:: Disclaimer: Use the following instructions as reference. Adapt the configuration for your network.

Installing the fib_optimizer
============================

To install the fib_optimizer we are going to use SWIX packages to simplify the operations::

    # Go to the management VRF if needed
    peer00.lab#routing-context vrf mgmtVRF
    peer00.lab(vrf:mgmtVRF)#copy https://github.com/dbarrosop/pySIR/releases/download/v0.45/pySIR-0.45-1.noarch.swix extension:
    Copy completed successfully.
    peer00.lab(vrf:mgmtVRF)#copy https://github.com/dbarrosop/sir_apps/releases/download/v0.1/fib_optimizer-0.1-1.noarch.swix extension:
    Copy completed successfully.
    peer00.lab(vrf:mgmtVRF)#extension pySIR-0.45-1.noarch.swix
    peer00.lab(vrf:mgmtVRF)#extension fib_optimizer-0.1-1.noarch.swix
    peer00.lab(vrf:mgmtVRF)#show extensions
    Name                                       Version/Release           Status extension
    ------------------------------------------ ------------------------- ------ ----
    fib_optimizer-0.1-1.noarch.swix            0.1/1                     A, I      1
    pmacct_sir-0.1-1.noarch.swix               0.1/1                     A, I      1
    pySIR-0.45-1.noarch.swix                   0.45/1                    A, I      1
    sir-0.17-1.noarch.swix                     0.17/1                    A, I      1

    A: available | NA: not available | I: installed | NI: not installed | F: forced

Configuring the fib_optimizer
=============================

To configure the fib_optimizer you will have to run some python code from some maching with access to the HTTPS port of
the switch.

First, install pySIR if you don't have it already::

    pip install pySIR

Now, execute inside your python shell the following code (modify the configuration parameters and base_url to meet your needs)::

    from pySIR.pySIR import pySIR
    import json

    base_url = 'https://peer00.lab/sir'
    configuration = {
        'lem_prefixes': '24',
        'max_lem_prefixes': 20000,
        'max_lpm_prefixes': 16000,
        'path': '/tmp/',
        'age': 168,
        'purge_older_than': 336,
    }
    sir = pySIR(base_url, verify_ssl=False)

    sir.post_variables('apps', 'fib_optimizer', content = json.dumps(configuration))

If you want to modify any variable later on you can run the following code in your python shell::

    from pySIR.pySIR import pySIR
    import json

    base_url = 'https://peer00.lab/sir'
    configuration = {
        'lem_prefixes': '24',
        'max_lem_prefixes': 40000,
        'max_lpm_prefixes': 16000,
        'path': '/tmp/',
        'age': 120,
        'purge_older_than': 240,
    }
    sir = pySIR(base_url, verify_ssl=False)

    sir.put_variables_by_category_and_name('apps', 'fib_optimizer', content = json.dumps(configuration))


Scheduling fib_optimizer
========================

In order to run the fib_optimizer hourly you will need to add the following line to your switch's configuration::

    schedule fib_optimizer at 09:05:00 08/17/2015 interval 60 max-log-files 48 command bash sudo ip netns exec ns-mgmtVRF /usr/local/bin/fib_optimizer.py https://127.0.0.1/sir

.. note:: If you get a comment saying ``! Schedule a command starting in past`` you can just ignore it.

.. note:: Replace ``ns-mgmtVRF`` with ``ns-$MGMT_VRF`` or ``default`` if you don't have any.

This command is going to schedule the fib_optimizer to run every hour. You can run the fib_optimizer outside the switch if you want, maybe in some server. In that case change the last argument to match the URL of SIR.

On every run, the fib_optimizer is going to create a few prefix-lists that we are going to use on a route-map to control SRD (Selective Route Download).

Configuring SRD
===============

SRD is a feature of some BGP implementations that allows you to pick some routers from the RIB and install them in the FIB. The routes not installed will still be processed as usual. This means that, if other policies permit it, they will be processed and forwarded to other BGP neighbors.

To enable SRD with EOS you only need to create a route-map (called SRD in our example) and execute::

    router bgp $YOUR_ASN
       bgp route install-map SRD

The content of the route-map can be anything, however, I recommend that you have at least::

    route-map SRD permit 10
       match as-path ASN_DC
    !
    route-map SRD permit 20
       match as-path ASN_TRANSIT
    !
    route-map SRD permit 30
       match ip address prefix-list fib_optimizer_lem_v4
    !
    route-map SRD permit 40
       match ip address prefix-list fib_optimizer_lpm_v4
    !

The first block is going to match the prefix-lists coming from your internal network, the second block is going to match the prefixes coming from your transit provider::

    ip as-path access-list ASN_DC permit ^$YOUR_INTERNAL_ASN$ any
    ip as-path access-list ASN_TRANSIT permit ^$YOUR_TRANSIT_ASN$ any

These two blocks are going to ensure that all prefixes coming from your DC are going to accepted and that the prefix coming from your transit provider (who is sending me the default route) is always installed. This will ensure that even if SIR or the fib_optimizer fails, I will still be able to route traffic.

The third and fourth block will be the ones controlled by the fib_optimizer.

.. warning:: Disclaimer: Take this as what it is, an example. Adapt the configuration for your network. This works for my network, it might not work for you. Even if you decide that this will work for you, you will still have to change the as-path list to match your own ASN's.
