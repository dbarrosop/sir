==================
Configuring pmacct
==================

Before installing pmacct we have to configure the Internet Router to send flow statistics via sFlow/Netflow to pmacct. In addition, we will have to configure the Internet Router to peer with pmacct and send all the prefixes coming from our peers.

^^^^^^^^^^^^^^^^^^^
Netflow/sFlow Agent
^^^^^^^^^^^^^^^^^^^

Configuring this agent on the Internet Router is out of the scope of this document. You should be able to find enough documentation on the Internet on how to do this with your network device.

^^^^^^^^^^^^^^^^^^^
Peering with pmacct
^^^^^^^^^^^^^^^^^^^

We will have to update bird configuration on the Internet Router in order to peer with pmacct. Doing that is very simple. Just add the following configuration to the file **/etc/bird/bird.conf** (you will probably have to update the IP's and the AS's)::

    #Pmacct
    protocol bgp {
        local as 65010;

        # As we are running pmacct on the same host we specify a different TCP port
        # In addition, pmacct works as an iBGP neighbor
        neighbor 10.0.1.10 port 1179 as 65010;

        # This will enable ADD-PATHs. If we have two routes for the same prefix
        # we will send all paths to pmacct instead of sending only the best path
        add paths tx;

        export filter {
            # We only want to send the prefixes coming from the peers
            if from = 10.0.0.2 then accept;
            reject;
        };
    }

^^^^^^^^^^^^^^^^^
Installing pmacct
^^^^^^^^^^^^^^^^^

Configuring pmacct is also out of the scope of this document. However, I am attaching some basic instructions I used to setup pmacct on my lab. To compile and install pmacct do the following::

    $ sudo apt-get install libpcap-dev make gcc libjansson-dev
    $ wget http://www.pmacct.net/pmacct-1.5.0.tar.gz
    $ tar xvzf pmacct-1.5.0.tar.gz
    $ cd pmacct-1.5.0/
    $ sudo mkdir -p /pmacct
    $ ./configure --prefix=/pmacct --enable-jansson
    $ make
    $ sudo make install

Finally, pmacct configuration might slightly differ depending on the protocol you are using to report flow statistics. In my example I am running fProbe as a netflow agent so I will be using netflow. We will need two files:

* **/pmacct/etc/nfacctd.conf**::

    daemonize: True

    # We use SQLite3 as backend
    plugins: sqlite3[simple]

    sql_db[simple]: /bgp_controller/bgpc.db
    sql_refresh_time[simple]: 3600
    sql_history[simple]: 60m
    sql_history_roundoff[simple]: h
    sql_table[simple]: acct

    aggregate: dst_net, dst_mask

    bgp_daemon: true
    bgp_daemon_ip: 10.0.1.10
    # As we are running pmacct on the same Internet Router we specify the port
    # If you are running pmacct on a dedicate machine you can skip this
    bgp_daemon_port: 1179
    bgp_daemon_max_peers: 2
    bgp_agent_map: /pmacct/etc/agent_to_peer.map
    bgp_table_dump_file: /bgp_controller/bgp/bgp-$peer_src_ip.txt
    bgp_table_dump_refresh_time: 3600

    nfacctd_as_new: bgp
    nfacctd_net: bgp
    # Port and IP to bind pmacct
    nfacctd_port: 9996
    nfacctd_ip: 127.0.0.1

* **/pmacct/etc/agent_to_peer.map**::

    # id=$BGP_ROUTER_ID_INTERNET ROUTER ip=$SRC_IP_FOR_NETFLOW_MESSAGES
    id=10.0.0.10	ip=127.0.0.1

Before starting pmacct we have to create the database::

    $ sqlite3 /bgp_controller/bgpc.db
    SQLite version 3.8.5 2014-08-15 22:37:57
    Enter ".help" for usage hints.
    sqlite> CREATE TABLE `acct` (
       ...>     `mac_src`   CHAR(17) NOT NULL DEFAULT '0:0:0:0:0:0',
       ...>     `mac_dst`   CHAR(17) NOT NULL DEFAULT '0:0:0:0:0:0',
       ...>     `ip_src`    CHAR(15) NOT NULL DEFAULT '0.0.0.0',
       ...>     `ip_dst`    CHAR(15) NOT NULL DEFAULT '0.0.0.0',
       ...>     `mask_dst`  INTEGER(1) NOT NULL DEFAULT 0,
       ...>     `src_port`  INT(4) NOT NULL DEFAULT 0,
       ...>     `dst_port`  INT(4) NOT NULL DEFAULT 0,
       ...>     `ip_proto`  CHAR(6) NOT NULL DEFAULT 0,
       ...>     `packets`   INT NOT NULL,
       ...>     `bytes` BIGINT NOT NULL,
       ...>     `stamp_inserted`    DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
       ...>     `stamp_updated` DATETIME,
       ...>     PRIMARY KEY(mac_src,mac_dst,ip_src,ip_dst,mask_dst,src_port,dst_port,ip_proto,stamp_inserted)
       ...> );
    sqlite> ^D
    $

Now you can start pmacct and check that it works::

    # Start pmacct
    $ sudo /pmacct/sbin/nfacctd -f /pmacct/etc/nfacctd.conf
    WARN ( default/core ): Daemonizing. Hmm, bye bye screen.

    # Check on the Internet Router that BGP is up
    $ sudo birdc
    BIRD 1.4.5 ready.
    bird> show protocols bgp4
    name     proto    table    state  since       info
    bgp4     BGP      master   up     18:31:28    Established

After an hour you should have data::

    $ sqlite3 /bgp_controller/bgpc.db
    SQLite version 3.8.2 2013-12-06 14:53:30
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite> SELECT count(*) from acct;
    21923
    sqlite> ^D
    $

    # BGP information
    $ ls /bgp_controller/bgp/
    bgp-10_0_1_10.txt

