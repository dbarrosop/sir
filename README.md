SDN Internet Router (sir)
=========================

SIR is an agent that you can run with any switch/router (either inside the switch or in some server close to the switch). The agent includes [pmacct](http://www.pmacct.net/) which allows you to correlate flows with the BGP table.


s tool in combination with [pmacct](http://www.pmacct.net/) allows you to get the full BGP feed from your upstream providers/peers and install on the FIB only the relevant prefixes for you. The main benefit of this approach is that you will not need a very expensive router to do peering. A cheap and very fast switch might be enough.



I recommend you to start reading the [How To: Simple Setup](http://sdn-internet-router-sir.readthedocs.org/en/latest/how_to_simple/index.html), there you can see what this is about, what you need and how to achieve it.

Although the following [video](http://youtu.be/o1njanXhQqM?list=PLXSSXAe33jI2IIWtfnnEj5J7B7KoixKCe) and [slides](docs/_static/SDN_Internet_Router-sir-Nov14.pdf) are old I suggest you to check them as that particular use case is still valid. Although the solution differs slightly from them.

Documentation
=============

You can find the documentation on [Read the Docs](http://sdn-internet-router-sir.readthedocs.org/en/latest/).


Note
====

This software is a release candidate. I don't expect big changes but the API might slightly change before the final release.
