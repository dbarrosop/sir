Configuring EOS
===============

No matter if you did the manual or the automated deployment you have to configure EOS to peer with pmacct and send sFlow
data::

    [dbarroso@lab tmp]$ exit
    logout
    lab# conf

    sflow sample dangerous 10000
    sflow polling-interval 1
    sflow destination 127.0.0.9 9999
    sflow source-interface $SOURCE_INTERFACE
    sflow run

    router bgp $AS
      neighbor 127.0.0.9 transport remote-port 1179
      neighbor 127.0.0.9 update-source $SOURCE_INTERFACE
      neighbor 127.0.0.9 remote-as $AS
      neighbor 127.0.0.9 description "SIR/pmacct"
      neighbor 127.0.0.9 maximum-routes 12000

.. warning:: Don't forget to replace ``$SOURCE_INTERFACE`` with the source-interface you want to use to connect from your device to the agent and ``$AS`` with your own AS.
