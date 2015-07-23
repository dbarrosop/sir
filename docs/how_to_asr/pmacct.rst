==================
Configuring pmacct
==================

First, we have to install `pmacct <http://www.pmacct.net/>`_ with JSON and BGP support. Compiling pmacct for your specific distro is out of the scope of this document but you can find below some instructions on how to do it for a debian based distro.

Installing dependancies
-----------------------

These are some of the dependancies that might need::

    apt-get install libpcap-dev libsqlite3-dev libjansson-dev zlib1g-dev

And this is how to compile pmacct:

    dbarroso@lon3-nwmonitor-a2:~$ wget http://www.pmacct.net/pmacct-1.5.1.tar.gz
    --2015-07-23 09:25:46--  http://www.pmacct.net/pmacct-1.5.1.tar.gz
    Connecting to 127.0.0.1:3128... connected.
    Proxy request sent, awaiting response... 200 OK
    Length: 874563 (854K) [application/x-gzip]
    Saving to: ‘pmacct-1.5.1.tar.gz’

    100%[==============================================================================>] 874,563     --.-K/s   in 0.09s

    2015-07-23 09:25:46 (9.80 MB/s) - ‘pmacct-1.5.1.tar.gz’ saved [874563/874563]

    dbarroso@lon3-nwmonitor-a2:~$ tar xzf pmacct-1.5.1.tar.gz
    dbarroso@lon3-nwmonitor-a2:~$ cd pmacct-1.5.1 --
    dbarroso@lon3-nwmonitor-a2:~/pmacct-1.5.1$ ./configure --enable-sqlite3 --enable-jansson --enable-ipv6 --prefix=/spotify/pmacct-1.5.1
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
    OS ........... : Linux 3.13.0-34-generic (lon3-nwmonitor-a2.lon3.spotify.net)
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
    dbarroso@lon3-nwmonitor-a2:~/pmacct-1.5.1$ make
    ...
    dbarroso@lon3-nwmonitor-a2:~/pmacct-1.5.1$ sudo make install
    ...
    dbarroso@lon3-nwmonitor-a2:~/pmacct-1.5.1$ cd /spotify/pmacct-1.5.1/
    dbarroso@lon3-nwmonitor-a2:/spotify/pmacct-1.5.1$ ls
    bin  sbin
