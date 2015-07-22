========
Features
========

The SDN Internet Router was designed to be extensible and pluggable from the beginning. The base system itself does not have that many features, it just provides a framework for backends and plugins to work with.

--------
Backends
--------

Backends provide the system a way of retrieving and storing data. In addition, they are who also provide the algorithm to select the best routes. You can only have one backend enable at a time. For more information, check the `backends documentation <../backends/index.html>`_.

-------
Plugins
-------

Plugins provide functionality to the system. A plugin will get all the information provided to the backend and do with it anything necessary. It could modify a BGP configuration to install prefixes by data sent/received, to prefer certain prefixes from certain peers, draw statistics of bytes/prefix, etc. For more information on available plugins and its functionality, check the `plugins documentation <../plugins/index.html>`_.
