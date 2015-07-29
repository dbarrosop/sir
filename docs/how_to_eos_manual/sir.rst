============
Enabling SIR
============

Installing SIR
--------------

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
------------

Instead of running our own HTTP and/or application server we are just going to use the services that EOS is already
using for their eAPI. For that you just have to copy a couple of configuration files that were provided in the same
tar file you downloaded before::

    [dbarroso@lab tmp]$ sudo cp eos_files/sir_uwsgi.ini /etc/uwsgi/
    [dbarroso@lab tmp]$ sudo cp eos_files/sir_nginx.conf /etc/nginx/external_conf/

Now, copy the configuration file for SIR::

    [dbarroso@lab tmp]$ sudo cp eos_files/sir_settings.py /mnt/drive/sir/settings.py

Starting the application server and SIR
---------------------------------------

To start SIR you just have to start application server::

[dbarroso@lab tmp]$ sudo SIR_SETTINGS='/mnt/drive/sir/settings.py' immortalize --daemonize --log=/var/log/sir.uwsgi.log /usr/bin/uwsgi --ini /etc/uwsgi/sir_uwsgi.ini

And finally you have to restart the HTTP server back in the EOS CLI. Assuming you already have the eAPI enabled::

    [dbarroso@lab tmp]$ exit
    logout
    lab#conf
    lab(config)#management api http-commands
    lab(config-mgmt-api-http-cmds)#shut
    lab(config-mgmt-api-http-cmds)#no shut

Accessing SIR
-------------

To access sir you just
