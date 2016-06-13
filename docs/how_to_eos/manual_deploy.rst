.. _Deploying SIR Manually:

Deploying SIR Manually
======================

If you want, you can deploy SIR manually. If you prefer to do it automatically go to the section
:ref:`Deploying SIR Automatically`.

.. warning:: Note that rebooting the switch will uninstall pmacct and SIR. The data will still be there but the software
             has to be installed after every reboot. That's why the automatic deployment is recommended.

pmacct
------

For simplicity I am providing both pmacct and the dependencies (jansson) precompiled. If you prefer you can compile
both yourself but that is outside the scope of this document. There are no changes from the original sources which you
can get in the following links:

* `pmacct <http://www.pmacct.net/pmacct-1.5.0.tar.gz>`_
* `jansson <http://www.digip.org/jansson/releases/jansson-2.7.tar.gz>`_

Getting pmacct
______________

First you have to get all the related configuration files and copy them to the correct location::

    lab#bash

    Arista Networks EOS shell

    [dbarroso@lab ~]$ cd /tmp/
    [dbarroso@lab tmp]$ sudo ip netns exec ns-mgmtVRF wget https://sdn-internet-router-sir.readthedocs.io/en/latest/_static/eos_files.tar.gz
    --2015-07-28 13:30:35--  https://sdn-internet-router-sir.readthedocs.io/en/latest/_static/eos_files.tar.gz
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
    [dbarroso@spine01 tmp]$ sudo cp eos_files/pmacct/libjansson.so.4 /usr/lib/
    [dbarroso@lab tmp]$ sudo mkdir -p /mnt/drive/sir/output/bgp/

If the database doesn't exist yet, now you can just copy the empty database::

    [dbarroso@lab tmp]$ sudo cp eos_files/pmacct/pmacct.db /mnt/drive/sir/output/

And finally, start pmacct::

    [dbarroso@lab tmp]$ sudo immortalize --log=/var/log/pmacct.log --daemonize /usr/sbin/sfacctd -f /etc/pmacct.conf


SIR
---

Installing SIR
______________

Installing SIR is very easy. You can install it by using PIP as any other python package::

    lab#bash

    Arista Networks EOS shell

    [dbarroso@lab ~]$ cd /tmp
    [dbarroso@lab tmp]$ sudo ip netns exec ns-mgmtVRF pip install SIR
    Downloading/unpacking SIR
      Downloading SIR-0.10.tar.gz (79kB): 79kB downloaded
      Running setup.py (path:/tmp/pip_build_root/SIR/setup.py) egg_info for package SIR
    ...
    Successfully installed SIR flask ipaddress Werkzeug Jinja2 itsdangerous MarkupSafe
    Cleaning up...

Enabling SIR
____________

Instead of running our own HTTP and/or application server we are just going to use the services that EOS is already
using for their eAPI. For that you just have to copy a couple of configuration files that were provided in the same
tar file you downloaded before::

    [dbarroso@lab tmp]$ sudo cp eos_files/sir_uwsgi.ini /etc/uwsgi/
    [dbarroso@lab tmp]$ sudo cp eos_files/sir_nginx.conf /etc/nginx/external_conf/

Now, copy the configuration file for SIR::

    [dbarroso@lab tmp]$ sudo cp eos_files/sir_settings.py /mnt/drive/sir/settings.py

Starting the application server and SIR
_______________________________________

To start SIR you just have to start application server::

[dbarroso@lab tmp]$ sudo SIR_SETTINGS='/mnt/drive/sir/settings.py' immortalize --daemonize --log=/var/log/sir.uwsgi.log /usr/bin/uwsgi --ini /etc/uwsgi/sir_uwsgi.ini

And finally you have to restart the HTTP server back in the EOS CLI. Assuming you already have the eAPI enabled::

    [dbarroso@lab tmp]$ exit
    logout
    lab#conf
    lab(config)#management api http-commands
    lab(config-mgmt-api-http-cmds)#shut
    lab(config-mgmt-api-http-cmds)#no shut
