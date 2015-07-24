A Software Defined Content Delivery Network
===========================================

As mentioned in the global architecture, you can aggregate the data exposed by SIR. This aggregated data can tell you
many things:

* Which networks are connecting to yours at what times.
* How much throughput they need.
* From where you can deliver your content to those networks.

This aggregated data could be sent to hadoop:

.. image:: sdcdn.png
    :align: center
    :alt: sdcdn

You could also add data from other sources. Things like:

* Cost of each link.
* Latency.
* Load of each site.
* Reliability.

Once all the data is in Hadoop you could try to analyze your global traffic pattern and metrics and redistribute
users to:

* Minimize transit costs.
* Maximize capacity usage.
* Improve user experience.
