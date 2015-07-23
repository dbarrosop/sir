===============
Enabling pmacct
===============

First, we have to install `pmacct <http://www.pmacct.net/>`_ with JSON, IPv6 and SQLite3 support. Compiling pmacct for your specific distro is out of the scope of this document but you can find below some instructions on how to do it for a debian based distro.

Compiling pmacct
----------------

These are some of the dependancies that might need::

    apt-get install libpcap-dev libsqlite3-dev libjansson-dev zlib1g-dev

And this is how to compile pmacct::

    $ wget http://www.pmacct.net/pmacct-1.5.1.tar.gz
    --2015-07-23 09:25:46--  http://www.pmacct.net/pmacct-1.5.1.tar.gz
    Connecting to 127.0.0.1:3128... connected.
    Proxy request sent, awaiting response... 200 OK
    Length: 874563 (854K) [application/x-gzip]
    Saving to: ‘pmacct-1.5.1.tar.gz’

    100%[==============================================================================>] 874,563     --.-K/s   in 0.09s

    2015-07-23 09:25:46 (9.80 MB/s) - ‘pmacct-1.5.1.tar.gz’ saved [874563/874563]

    $ tar xzf pmacct-1.5.1.tar.gz
    $ cd pmacct-1.5.1
    $ ./configure --enable-sqlite3 --enable-jansson --enable-ipv6 --prefix=/pmacct-1.5.1
    creating cache ./config.cache
    checking for a BSD compatible install... /usr/bin/install -c
    checking whether build environment is sane... yes
    checking whether make sets ${MAKE}... yes
    checking for working aclocal-1.4... missing
    checking for working autoconf... missing
    checking for working automake-1.4... missing
    checking for working autoheader... missing
    checking for working makeinfo... missing
    checking for gcc... gcc
    checking whether the C compiler (gcc  ) works... yes
    checking whether the C compiler (gcc  ) is a cross-compiler... no
    checking whether we are using GNU C... yes
    checking whether gcc accepts -g... yes
    checking OS... Linux
    checking hardware... x86_64
    checking for ranlib... ranlib
    checking whether to enable debugging compiler options... no
    checking whether to relax compiler optimizations... no
    checking whether to disable linking against shared objects... no
    checking for dlopen... no
    checking for dlopen in -ldl... yes
    checking for gmake... no
    checking for make... make
    checking whether make sets ${MAKE}... (cached) yes
    checking for __progname... yes
    checking for extra flags needed to export symbols... --export-dynamic
    checking for static inline... yes
    checking endianess... little
    checking unaligned accesses... ok
    checking whether to enable L2 features... yes
    checking whether to enable IPv6 code... yes
    checking for inet_pton... yes
    checking for inet_ntop... yes
    checking whether to enable IPv4-mapped IPv6 sockets ... yes
    checking whether to enable IP prefix labels... checking default locations for pcap.h... found in /usr/include
    checking default locations for libpcap... no
    checking for pcap_dispatch in -lpcap... yes
    checking for pcap_setnonblock in -lpcap... yes
    checking packet capture type... linux
    checking whether to enable MySQL support... checking how to run the C preprocessor... gcc -E
    no
    checking whether to enable PostgreSQL support... no
    checking whether to enable MongoDB support... no
    checking whether to enable SQLite3 support... yes
    checking default locations for libsqlite3... not found
    checking for sqlite3_open in -lsqlite3... yes
    checking default locations for sqlite3.h... found in /usr/include
    checking whether to enable RabbitMQ/AMQP support... no
    checking whether to enable GeoIP support... no
    checking whether to enable Jansson support... yes
    checking default locations for Jansson library... not found
    checking for json_object in -ljansson... yes
    checking default locations for jansson.h... found in /usr/include
    checking for ANSI C header files... no
    checking for sys/wait.h that is POSIX.1 compatible... yes
    checking for getopt.h... yes
    checking for sys/select.h... yes
    checking for sys/time.h... yes
    checking for u_int64_t in sys/types.h... yes
    checking for u_int32_t in sys/types.h... yes
    checking for u_int16_t in sys/types.h... yes
    checking for u_int8_t in sys/types.h... yes
    checking for uint64_t in sys/types.h... no
    checking for uint32_t in sys/types.h... no
    checking for uint16_t in sys/types.h... no
    checking for uint8_t in sys/types.h... no
    checking whether to enable 64bit counters... yes
    checking whether to enable multithreading in pmacct... yes
    checking whether to enable ULOG support... no
    checking return type of signal handlers... void
    checking for strlcpy... no
    checking for vsnprintf... no
    checking for setproctitle... no
    checking for mallopt... no

    PLATFORM ..... : x86_64
    OS ........... : Linux 3.13.0-34-generic
    COMPILER ..... : gcc
    CFLAGS ....... : -O2 -g -O2
    LIBS ......... : -ljansson -lsqlite3 -lpcap  -ldl -lm -lz -lpthread
    SERVER_LIBS ...: -lnfprobe_plugin -Lnfprobe_plugin/ -lsfprobe_plugin -Lsfprobe_plugin/ -lbgp -Lbgp/ -ltee_plugin -Ltee_plugin/ -lisis -Lisis/ -lbmp -Lbmp/
    LDFLAGS ...... : -Wl,--export-dynamic

    Now type 'make' to compile the source code.

    Are you willing to get in touch with other pmacct users?
    Join the pmacct mailing-list by sending a message to pmacct-discussion-subscribe@pmacct.net

    Need for documentation and examples?
    Read the README file or go to http://wiki.pmacct.net/


    updating cache ./config.cache
    creating ./config.status
    creating Makefile
    creating src/Makefile
    creating src/nfprobe_plugin/Makefile
    creating src/sfprobe_plugin/Makefile
    creating src/bgp/Makefile
    creating src/tee_plugin/Makefile
    creating src/isis/Makefile
    creating src/bmp/Makefile
    $ make
    ... (output omitted for clarity)
    $ sudo make install
    ... (output omitted for clarity)

Configuring pmacct
------------------

To configure pmacct you will need to know the IP the ASR will use as source IP for both netflow and BGP. Once you know, paste the following configuration in the file ``/pmacct-1.5.1/etc/pmacct.conf``::

    $ cd /pmacct-1.5.1
    $ sudo mkdir etc
    $ sudo vi etc/pmacct.conf
    daemonize: true

    plugins: sqlite3[simple]

    sql_db[simple]: /pmacct-1.5.1/output/pmacct.db
    sql_refresh_time[simple]: 3600
    sql_history[simple]: 60m
    sql_history_roundoff[simple]: h
    sql_table[simple]: acct
    sql_table_version[simple]: 9

    aggregate: dst_net, dst_mask, dst_as

    bgp_daemon: true
    bgp_daemon_ip: $ASR_SRC_IP
    bgp_daemon_max_peers: 2
    bgp_table_dump_file: /pmacct-1.5.1/output/bgp-$peer_src_ip-%Y_%m_%dT%H_%M_%S.txt
    bgp_table_dump_refresh_time: 3600

    nfacctd_as_new: bgp
    nfacctd_net: bgp
    nfacctd_port: 9999
    nfacctd_ip: $ASR_SRC_IP
    nfacctd_time_new: true

.. warning:: Don't forget to replace ``$ASR_SRC_IP`` with the IP your ASR will use for both netflow and BGP.

Now it's time to setup the database::

    $ sudo mkdir output
    $ sudo sqlite3 output/pmacct.db << EOF
    CREATE TABLE 'acct' (
    	'tag'	INT(8) NOT NULL DEFAULT 0,
    	'class_id'	CHAR(16) NOT NULL DEFAULT ' ',
    	'mac_src'	CHAR(17) NOT NULL DEFAULT '0:0:0:0:0:0',
    	'mac_dst'	CHAR(17) NOT NULL DEFAULT '0:0:0:0:0:0',
    	'vlan'	INT(4) NOT NULL DEFAULT 0,
    	'as_src'	INT(8) NOT NULL DEFAULT 0,
    	'as_dst'	INT(8) NOT NULL DEFAULT 0,
    	'ip_src'	CHAR(15) NOT NULL DEFAULT '0.0.0.0',
    	'ip_dst'	CHAR(15) NOT NULL DEFAULT '0.0.0.0',
    	'mask_dst'	INTEGER(1) NOT NULL DEFAULT 0,
    	'port_src'	INT(4) NOT NULL DEFAULT 0,
    	'port_dst'	INT(4) NOT NULL DEFAULT 0,
    	'tcp_flags'	INT(4) NOT NULL DEFAULT 0,
    	'ip_proto'	CHAR(6) NOT NULL DEFAULT 0,
    	'tos'	INT(4) NOT NULL DEFAULT 0,
    	'packets'	INT NOT NULL,
    	'bytes'	BIGINT NOT NULL,
    	'flows'	INT NOT NULL DEFAULT 0,
    	'stamp_inserted'	DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
    	'stamp_updated'	DATETIME,
    	'collumn'	peer_as_srcINT(8) NOT NULL DEFAULT 0,
    	'peer_as_dst'	INT(8) NOT NULL DEFAULT 0,
    	'peer_as_src'	INT(8) NOT NULL DEFAULT 0,
    	'peer_dst_ip'	TEXT NOT NULL DEFAULT '0.0.0.0',
    	PRIMARY KEY(tag,class_id,mac_src,mac_dst,vlan,as_src,as_dst,ip_src,ip_dst,mask_dst,port_src,port_dst,ip_proto,tos,stamp_inserted)
    );
    CREATE TABLE 'variables' (
    	'name'	TEXT,
    	'content'	TEXT,
    	'category'	TEXT,
    	PRIMARY KEY(name,category)
    );

    CREATE INDEX acct_idx1 ON acct(stamp_updated);
    CREATE INDEX acct_idx2 ON acct(stamp_updated, as_dst);
    CREATE INDEX acct_idx3 ON acct(stamp_updated, ip_dst, mask_dst);

    CREATE INDEX variables_idx1 ON variables(category);
    EOF

Finally, it's just a matter of starting pmacct::

    $ sudo /pmacct-1.5.1/sbin/nfacctd -f /pmacct-1.5.1/etc/pmacct.conf

Configuring the ASR
-------------------

Configuring the ASR is relatively easy, you only have to configure netflow to send the flows that you want to process and BGP to send the prefixes you want to use for the aggregation. Here is an example::

    flow exporter-map SIR
     version v9
      options interface-table timeout 60
      template data timeout 60
     !
     transport udp 9999
     source Loopback0
     destination $PMACCT_IP
    !
    flow monitor-map SIR-FMM
     record ipv4
     exporter SIR
     cache timeout active 60
     cache timeout inactive 15
    !
    sampler-map SIR
     random 1 out-of 10000

    interface HundredGigE0/0/0/1
     flow ipv4 monitor SIR-FMM sampler SIR egress

    route-policy PASS
      pass
    end-policy

    route-policy BLOCK
      drop
    end-policy

    router bgp $AS
      neighbor $PMACCT_IP
       remote-as $AS
       description SIR
       update-source Loopback0
       address-family ipv4 unicast
        route-policy BLOCK in
        route-policy PASS out

.. warning:: Don't forget to replace ``$PMACCT_IP`` with the IP of the server where you are running pmacct and ``$AS`` with your own AS.
