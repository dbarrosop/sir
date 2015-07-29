=================
Installing pmacct
=================

For simplicity I am providing both pmacct and the dependencies (jansson) precompiled. If you prefer you can compile
both yourself but that is outside the scope of this document. There are no changes from the original source which you
can get in the following links:

* `pmacct <http://www.pmacct.net/pmacct-1.5.0.tar.gz>`_
* `jansson <http://www.digip.org/jansson/releases/jansson-2.7.tar.gz>`_

Getting pmacct
--------------

First you have to get all the related configuration files and copy them to the correct location::

    lab#bash

    Arista Networks EOS shell

    [dbarroso@lab ~]$ cd /tmp/
    [dbarroso@lab tmp]$ sudo ip netns exec ns-mgmtVRF wget http://sdn-internet-router-sir.readthedocs.org/en/latest/_static/eos_files.tar.gz
    --2015-07-28 13:30:35--  http://sdn-internet-router-sir.readthedocs.org/en/latest/_static/eos_files.tar.gz
    Resolving sdn-internet-router-sir.readthedocs.org... 162.209.114.75
    Connecting to sdn-internet-router-sir.readthedocs.org|162.209.114.75|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 1341140 (1.3M) [application/octet-stream]
    Saving to: `eos_files.tar.gz'

    100%[========================================================================================================================================================================================>] 1,341,140    833K/s   in 1.6s

    2015-07-28 13:30:37 (833 KB/s) - `eos_files.tar.gz' saved [1341140/1341140]

    [dbarroso@lab tmp]$ tar xvzf eos_files.tar.gz
    eos_files/
    eos_files/._.DS_Store
    eos_files/.DS_Store
    eos_files/pmacct/
    eos_files/sir_nginx.conf
    eos_files/sir_settings.py
    eos_files/sir_uwsgi.ini
    eos_files/pmacct/._.DS_Store
    eos_files/pmacct/.DS_Store
    eos_files/pmacct/libjansson.so.4
    eos_files/pmacct/pmacct
    eos_files/pmacct/pmacct.conf
    eos_files/pmacct/pmacct.db
    eos_files/pmacct/sfacctd

    [dbarroso@lab tmp]$ sudo cp eos_files/pmacct/pmacct.conf /etc/
    [dbarroso@lab tmp]$ sudo cp eos_files/pmacct/pmacct /usr/bin/
    [dbarroso@lab tmp]$ sudo cp eos_files/pmacct/sfacctd /usr/sbin/
    [dbarroso@lab tmp]$ sudo mkdir -p /mnt/drive/sir/output/bgp/

If the database doesn't exist yet, now you can just copy the empty database::

    [dbarroso@lab tmp]$ sudo cp eos_files/pmacct/pmacct.db /mnt/drive/sir/output/

And finally, start pmacct::

    [dbarroso@lab tmp]$ sudo immortalize --log=/var/log/pmacct.log --daemonize /usr/sbin/sfacctd -f /etc/pmacct.conf

Configuring EOS
---------------

Now go back to EOS CLI and configure sflow and BGP::

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

.. warning:: Don't forget to replace ``$$SOURCE_INTERFACE`` with the source-interface you want to use to connect from your device to the agent and ``$AS`` with your own AS.
