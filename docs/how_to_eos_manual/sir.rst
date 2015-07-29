============
Enabling SIR
============

Installing SIR
--------------

Installing SIR is very easy. You can install it by using PIP as any other python package::

    spine01#bash

    Arista Networks EOS shell

    [dbarroso@spine01 ~]$ cd /tmp
    [dbarroso@spine01 tmp]$ sudo ip netns exec ns-mgmtVRF pip install SIR
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

    [dbarroso@spine01 tmp]$ sudo cp eos_files/sir_uwsgi.ini /etc/uwsgi/
    [dbarroso@spine01 tmp]$ sudo cp eos_files/sir_nginx.conf /etc/nginx/external_conf/

Now, copy the configuration file for SIR::

    [dbarroso@spine01 tmp]$ sudo cp eos_files/sir_settings.py /mnt/drive/sir/settings.py

Starting the application server and SIR
---------------------------------------

To start SIR you just have to start application server::

[dbarroso@spine01 tmp]$ sudo SIR_SETTINGS='/mnt/drive/sir/settings.py' immortalize --daemonize --log=/var/log/sir.uwsgi.log /usr/bin/uwsgi --ini /etc/uwsgi/sir_uwsgi.ini

And finally you have to restart the HTTP server back in the EOS CLI::

    [dbarroso@spine01 tmp]$ exit
    logout
    spine01#conf
    spine01(config)#management api http-commands
    spine01(config-mgmt-api-http-cmds)#shut
    spine01(config-mgmt-api-http-cmds)#no shut
