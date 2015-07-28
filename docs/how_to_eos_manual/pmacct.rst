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

::
    peer00.lon#bash

    Arista Networks EOS shell

    [dbarroso@peer00 ~]$ mkdir /mnt/drive/sir
    [dbarroso@peer00 ~]$ cd /mnt/drive/sir
    [dbarroso@spine01 sir]$ sudo ip netns exec ns-mgmtVRF wget -O pmacct-1.5.0_eos4.tar.gz https://github.com/dbarrosop/sir/releases/download/v0.9/pmacct-1.5.0_eos4.tar.gz
    --2015-07-27 09:44:42--  https://github.com/dbarrosop/sir/releases/download/v0.9/pmacct-1.5.0_eos4.tar.gz
    Resolving github.com... 192.30.252.130
    Connecting to github.com|192.30.252.130|:443... connected.
    HTTP request sent, awaiting response... 302 Found
    Location: https://s3.amazonaws.com/github-cloud/releases/27316436/a264b2d8-3452-11e5-9c86-ed1fae0d2f79.gz?response-content-disposition=attachment%3B%20filename%3Dpmacct-1.5.0_eos4.tar.gz&response-content-type=application/octet-stream&AWSAccessKeyId=AKIAISTNZFOVBIJMK3TQ&Expires=1437990342&Signature=cxgOmyn8BBVky2bZlzOs4ey2tC8%3D [following]
    --2015-07-27 09:44:42--  https://s3.amazonaws.com/github-cloud/releases/27316436/a264b2d8-3452-11e5-9c86-ed1fae0d2f79.gz?response-content-disposition=attachment%3B%20filename%3Dpmacct-1.5.0_eos4.tar.gz&response-content-type=application/octet-stream&AWSAccessKeyId=AKIAISTNZFOVBIJMK3TQ&Expires=1437990342&Signature=cxgOmyn8BBVky2bZlzOs4ey2tC8%3D
    Resolving s3.amazonaws.com... 54.231.33.16
    Connecting to s3.amazonaws.com|54.231.33.16|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 4921495 (4.7M) [application/octet-stream]
    Saving to: `pmacct-1.5.0_eos4.tar.gz'

    100%[=====================================================================================================================================================================================================>] 4,921,495   1.79M/s   in 2.6s

    2015-07-27 09:44:45 (1.79 MB/s) - `pmacct-1.5.0_eos4.tar.gz' saved [4921495/4921495]

    [dbarroso@spine01 sir]$ tar xvzf pmacct-1.5.0_eos4.tar.gz
    pmacct/
    pmacct/bin/
    pmacct/etc/
    pmacct/lib/
    pmacct/output/
    pmacct/sbin/
    pmacct/sbin/nfacctd
    pmacct/sbin/pmacctd
    pmacct/sbin/sfacctd
    pmacct/sbin/start_pmacct.sh
    pmacct/sbin/uacctd
    pmacct/output/pmacct.db
    pmacct/lib/libjansson.so.4
    pmacct/etc/pmacct.conf
    pmacct/bin/pmacct

Enabling pmacct
---------------

::
    daemon pmacct
       exec /mnt/drive/sir/pmacct/sbin/start_pmacct.sh
       no shutdown

    sflow sample dangerous 10000
    sflow polling-interval 1
    sflow destination 127.0.0.9 9999
    sflow source-interface Ethernet47
    sflow run

    router bgp $AS
      neighbor 127.0.0.9 remote-as $AS
      neighbor 127.0.0.9 description "SIR/pmacct"
      neighbor 127.0.0.9 transport remote-port 1179
      neighbor 127.0.0.9 update-source Ethernet47
      neighbor 127.0.0.9 maximum-routes 12000

.. warning:: Don't forget to replace ``$AS`` with your own AS.
