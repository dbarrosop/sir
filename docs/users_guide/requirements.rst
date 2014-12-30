============
Requirements
============

-------------------
The Internet Router
-------------------

You can use any router or L3 switch you want. The more LPM routes you can afford, the better, however, you are not bounded by that.
The Internet will require:

 * BGP

    - All BGP feature required by your network design.
    - Selective Route Download.

 * Export flow statistics. Any mean supported by pmacct_.

------------------
The BGP Controller
------------------


The BGP Controller will require:

 * pmacct_.
 * sir (python2.7).


.. _pmacct: http://www.pmacct.net/