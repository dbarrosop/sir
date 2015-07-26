A commodity switch as a Peering Router
======================================

This is a simple and interesting use case. Once you start collecting data in your peering routers you will quickly
realize that you don't use more than 30.000 prefixes daily. So why do you need a big and expensive router to hold
the full routing table? Wouldn't be better and easier (and most probably cheaper) to hold the full routing table in
the RIB and just install the routes you need in the FIB?

With SIR you can easily see how many routes you need to offload your traffic and which routes you will need. Once
you have this information it's just a matter of instructing your switch to accept those prefixes and keep the rest in
memory.

.. image:: peering_router.png
    :align: center
    :alt: peering_router

You can do that in different ways, being SRD the most stable and simplest way. Soon I will share an app that leverages
on SIR to convert a cheap Arista 7280 switch into a peering router.

This was the original purpose when I started SIR. Although the scope of SIR has changed (before it was a monolitic app
and now it's an agent that provides information via an aPI) you can see a presentation and a podcast about this topic
in the following links:

* `<http://youtu.be/o1njanXhQqM>`_
* `<http://blog.ipspace.net/2015/01/sdn-router-spotify-on-software-gone-wild.html>`_
