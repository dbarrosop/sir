.. _Deploying SIR Automatically:

Deploying SIR Automatically
===========================

If you want, you can deploy SIR automatically. If you prefer to do it manually go to the section
:ref:`Deploying SIR Manually`.

Deployment script
-----------------

The automated deployment is done via a bash script. First thing you have to do is download it::

  lab.lon#bash

  Arista Networks EOS shell

  [dbarroso@lab ~]$ cd /mnt/flash
  [dbarroso@lab flash]$ wget -O /mnt/flash/deploy_sir_eos.sh https://raw.githubusercontent.com/dbarrosop/sir/master/scripts/deploy_sir_eos.sh
  --2015-07-30 10:18:51--  https://raw.githubusercontent.com/dbarrosop/sir/master/scripts/deploy_sir_eos.sh
  Resolving raw.githubusercontent.com... 185.31.18.133
  Connecting to raw.githubusercontent.com|185.31.18.133|:443... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 3768 (3.7K) [text/plain]
  Saving to: `/mnt/flash/deploy_sir_eos.sh'

  100%[============================================================================================>] 3,768       --.-K/s   in 0s

  2015-07-30 10:18:51 (322 MB/s) - `/mnt/flash/deploy_sir_eos.sh' saved [3768/3768]

  [dbarroso@lab flash]$ sudo chmod +x /mnt/flash/deploy_sir_eos.sh

.. note:: If you have your management inside a VRF prepend ``sudo ip netns exec ns-$MGMT_VRF_NAME`` before
          ``wget``, where ``$MGMT_VRF_NAME`` is the name of your management VRF, i.e., ``sudo ip netns exec
          ns-mgmtVRF wget...```

Now, you can just use that script to deploy SIR automatically. Check the help first::

    [dbarroso@lab flash]$ /mnt/flash/deploy_sir_eos.sh --help
    Usage: /mnt/flash/deploy_sir_eos.sh
    Optional arguments:
    	-h|--help            # This help.
    	--vrf=VRF_NAME       # If you are using a management VRF specify the name here.
    	--sir=SIR_PATH       # If you want to install SIR from a local file specify the path here. Otherwise the latest version will be downloaded from the Internet.
    	--pmacct=PMACCT_PATH # If you want to install pmacct from a local file specify the path here. Otherwise the latest version will be downloaded from the Internet.
      -r|--restart-pmacct  # If set it will restart pmacct.
      -u|--upgrade-sir     # If set it will upgrade SIR and all its dependencies. If you are installing SIR from a file it will upgrade only its dependencies.

And using the options that you want execute the script::

    [dbarroso@lab flash]$ sudo /mnt/flash/deploy_sir_eos.sh
    Downloading eos_file from http://sdn-internet-router-sir.readthedocs.org/en/latest/_static/eos_files.tar.gz
    --2015-07-30 07:23:33--  http://sdn-internet-router-sir.readthedocs.org/en/latest/_static/eos_files.tar.gz
    Resolving sdn-internet-router-sir.readthedocs.org... 162.209.114.75
    Connecting to sdn-internet-router-sir.readthedocs.org|162.209.114.75|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 1341140 (1.3M) [application/octet-stream]
    Saving to: `/tmp/eos_files.tar.gz'

         0K .......... .......... .......... .......... ..........  3%  274K 5s
        50K .......... .......... .......... .......... ..........  7%  544K 3s
       100K .......... .......... .......... .......... .......... 11%  549K 3s
       150K .......... .......... .......... .......... .......... 15% 11.4M 2s
       200K .......... .......... .......... .......... .......... 19%  566K 2s
       250K .......... .......... .......... .......... .......... 22% 10.1M 2s
       300K .......... .......... .......... .......... .......... 26%  582K 2s
       350K .......... .......... .......... .......... .......... 30% 11.0M 1s
       400K .......... .......... .......... .......... .......... 34% 11.4M 1s
       450K .......... .......... .......... .......... .......... 38%  614K 1s
       500K .......... .......... .......... .......... .......... 41% 9.66M 1s
       550K .......... .......... .......... .......... .......... 45% 9.62M 1s
       600K .......... .......... .......... .......... .......... 49% 11.3M 1s
       650K .......... .......... .......... .......... .......... 53%  642K 1s
       700K .......... .......... .......... .......... .......... 57% 11.4M 1s
       750K .......... .......... .......... .......... .......... 61% 11.3M 0s
       800K .......... .......... .......... .......... .......... 64% 11.0M 0s
       850K .......... .......... .......... .......... .......... 68%  523K 0s
       900K .......... .......... .......... .......... .......... 72%  913K 0s
       950K .......... .......... .......... .......... .......... 76%  151M 0s
      1000K .......... .......... .......... .......... .......... 80%  203M 0s
      1050K .......... .......... .......... .......... .......... 83%  127M 0s
      1100K .......... .......... .......... .......... .......... 87%  180M 0s
      1150K .......... .......... .......... .......... .......... 91%  187M 0s
      1200K .......... .......... .......... .......... .......... 95%  173M 0s
      1250K .......... .......... .......... .......... .......... 99%  277K 0s
      1300K .........                                             100% 12.9M=1.1s

    2015-07-30 07:23:35 (1.19 MB/s) - `/tmp/eos_files.tar.gz' saved [1341140/1341140]

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

    Installing pmacct

    Starting sfacctd: done

    Installing latest SIR from PIP
    Downloading/unpacking SIR
      Running setup.py (path:/tmp/pip_build_root/SIR/setup.py) egg_info for package SIR

    Downloading/unpacking flask (from SIR)
      Running setup.py (path:/tmp/pip_build_root/flask/setup.py) egg_info for package flask

        warning: no files found matching '*' under directory 'tests'
        warning: no previously-included files matching '*.pyc' found under directory 'docs'
        warning: no previously-included files matching '*.pyo' found under directory 'docs'
        warning: no previously-included files matching '*.pyc' found under directory 'tests'
        warning: no previously-included files matching '*.pyo' found under directory 'tests'
        warning: no previously-included files matching '*.pyc' found under directory 'examples'
        warning: no previously-included files matching '*.pyo' found under directory 'examples'
        no previously-included directories found matching 'docs/_build'
        no previously-included directories found matching 'docs/_themes/.git'
    Downloading/unpacking ipaddress (from SIR)
      Downloading ipaddress-1.0.14-py27-none-any.whl
    Requirement already satisfied (use --upgrade to upgrade): PyYAML in /usr/lib/python2.7/site-packages (from SIR)
    Downloading/unpacking Werkzeug>=0.7 (from flask->SIR)
    Downloading/unpacking Jinja2>=2.4 (from flask->SIR)
    Downloading/unpacking itsdangerous>=0.21 (from flask->SIR)
      Running setup.py (path:/tmp/pip_build_root/itsdangerous/setup.py) egg_info for package itsdangerous

        warning: no previously-included files matching '*' found under directory 'docs/_build'
    Downloading/unpacking MarkupSafe (from Jinja2>=2.4->flask->SIR)
      Downloading MarkupSafe-0.23.tar.gz
      Running setup.py (path:/tmp/pip_build_root/MarkupSafe/setup.py) egg_info for package MarkupSafe

    Installing collected packages: SIR, flask, ipaddress, Werkzeug, Jinja2, itsdangerous, MarkupSafe
      Running setup.py install for SIR

      Running setup.py install for flask

        warning: no files found matching '*' under directory 'tests'
        warning: no previously-included files matching '*.pyc' found under directory 'docs'
        warning: no previously-included files matching '*.pyo' found under directory 'docs'
        warning: no previously-included files matching '*.pyc' found under directory 'tests'
        warning: no previously-included files matching '*.pyo' found under directory 'tests'
        warning: no previously-included files matching '*.pyc' found under directory 'examples'
        warning: no previously-included files matching '*.pyo' found under directory 'examples'
        no previously-included directories found matching 'docs/_build'
        no previously-included directories found matching 'docs/_themes/.git'
      Running setup.py install for itsdangerous

        warning: no previously-included files matching '*' found under directory 'docs/_build'
      Running setup.py install for MarkupSafe

        building 'markupsafe._speedups' extension
        gcc -pthread -fno-strict-aliasing -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector -fno-var-tracking -fno-var-tracking-assignments --param=ssp-buffer-size=4 -m32 -march=i686 -mtune=atom -fasynchronous-unwind-tables -O2 -D_GNU_SOURCE -fPIC -fwrapv -DNDEBUG -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector -fno-var-tracking -fno-var-tracking-assignments --param=ssp-buffer-size=4 -m32 -march=i686 -mtune=atom -fasynchronous-unwind-tables -O2 -D_GNU_SOURCE -fPIC -fwrapv -fPIC -I/usr/include/python2.7 -c markupsafe/_speedups.c -o build/temp.linux-x86_64-2.7/markupsafe/_speedups.o
        unable to execute gcc: No such file or directory
        ==========================================================================
        WARNING: The C extension could not be compiled, speedups are not enabled.
        Failure information, if any, is above.
        Retrying the build without the C extension now.


        ==========================================================================
        WARNING: The C extension could not be compiled, speedups are not enabled.
        Plain-Python installation succeeded.
        ==========================================================================
    Successfully installed SIR flask ipaddress Werkzeug Jinja2 itsdangerous MarkupSafe
    Cleaning up...

    Copying configuration files for SIR
    Starting SIR
    Restarting nginx

If everything went fine SIR should be accessible as it is explained in the section :ref:`accessing_sir`.

Automatic install at boot time
------------------------------

As mentioned in the previous section, the data is saved in the permanent storage of the device but the software is
installed in a file system that is wiped out at every boot. To install the software at boot time automatically we can
just add a task on EOS::

    event-handler install_sir
       trigger on-boot
       action bash sudo /mnt/flash/deploy_sir_eos.sh --vrf=mgmtVRF &> /tmp/deploy_sir_eos.log
       delay 300
       timeout 120

That will install the software every time the switch boots. You can check if the deployment happened with the command::

    lab#show event-handler install_sir
    Event-handler install_sir
    Trigger: on-boot delay 300 seconds
    Action: sudo /mnt/flash/deploy_sir_eos.sh --vrf=mgmtVRF --vrf=mgmtVRF --sir=/mnt/flash/sir/sir-0.11/ --pmacct=/mnt/flash/sir/eos_files/ &> /tmp/deploy_sir_eos.log
    Action expected to finish in less than 120 seconds
    Last Trigger Activation Time: 5 minutes 3 seconds ago
    Total Trigger Activations: 1
    Last Action Time: 3 seconds ago
    Total Actions: 1

You can also check how the deployment went in the log file ``/tmp/deploy_sir_eos.log``::

    lab#bash tail /tmp/deploy_sir_eos.log
    Searching for PyYAML==3.09
    Best match: PyYAML 3.09
    Adding PyYAML 3.09 to easy-install.pth file

    Using /usr/lib/python2.7/site-packages
    Finished processing dependencies for SIR==0.10

    Copying configuration files for SIR
    Starting SIR
    Restarting nginx

Using local software
--------------------

If you are using this in production I recommend you to use local data instead of downloading the software from the
Internet every time. The main reason is that the script will always download the latest version so it's safer for
production to get the software yourself, save it in the flash and ask the script to deploy it. To do that you can do
something like this::

    lab.lon#bash

    Arista Networks EOS shell

    [dbarroso@lab ~]$ cd /mnt/flash
    [dbarroso@lab flash]$ mkdir sir
    [dbarroso@lab flash]$ cd sir/
    [dbarroso@lab sir]$ wget -O sir.tar.gz https://github.com/dbarrosop/sir/archive/v0.11.tar.gz
    ...
    2015-07-30 10:41:55 (1.16 MB/s) - `sir.tar.gz' saved [4091306]

    [dbarroso@lab sir]$ tar xvzf sir.tar.gz
    ...
    [dbarroso@lab sir]$ wget http://sdn-internet-router-sir.readthedocs.org/en/latest/_static/eos_files.tar.gz
    ...
    2015-07-30 10:42:35 (1.36 MB/s) - `eos_files.tar.gz' saved [1341140/1341140]
    [dbarroso@lab sir]$ tar xvzf eos_files.tar.gz
    ...
    [dbarroso@lab sir]$ sudo /mnt/flash/deploy_sir_eos.sh --vrf=mgmtVRF --sir=/mnt/flash/sir/sir-0.11/ --pmacct=/mnt/flash/sir/eos_files/
    Using local eos_file: /mnt/flash/sir/eos_files/

    Installing pmacct

    Starting sfacctd: sfacctd was already running

    Installing SIR from local folder: /mnt/flash/sir/sir-0.11/
    ...

    Copying configuration files for SIR
    Stopping SIR
    Starting SIR
    Restarting nginx

If you are using local data to deploy SIR don't forget to modify the ``event-handler`` accordingly::

    event-handler install_sir
       trigger on-boot
       action bash sudo /mnt/flash/deploy_sir_eos.sh --vrf=mgmtVRF --vrf=mgmtVRF --sir=/mnt/flash/sir/sir-0.11/ --pmacct=/mnt/flash/sir/eos_files/ &> /tmp/deploy_sir_eos.log
       delay 300
       timeout 120
