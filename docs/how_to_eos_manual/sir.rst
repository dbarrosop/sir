::
[dbarroso@peer00 sir]$ sudo ip netns exec ns-mgmtVRF wget -O v0.9.tar.gz https://github.com/dbarrosop/sir/archive/v0.9.tar.gz
--2015-07-27 10:33:59--  https://github.com/dbarrosop/sir/archive/v0.9.tar.gz
Resolving github.com... 192.30.252.129
Connecting to github.com|192.30.252.129|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://codeload.github.com/dbarrosop/sir/tar.gz/v0.9 [following]
--2015-07-27 10:33:59--  https://codeload.github.com/dbarrosop/sir/tar.gz/v0.9
Resolving codeload.github.com... 192.30.252.144
Connecting to codeload.github.com|192.30.252.144|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2745299 (2.6M) [application/x-gzip]
Saving to: `v0.9.tar.gz'

100%[=====================================================================================================================================================================================================>] 2,745,299   1.37M/s   in 1.9s

2015-07-27 10:34:01 (1.37 MB/s) - `v0.9.tar.gz' saved [2745299/2745299]

[dbarroso@peer00 sir]$ tar xvzf v0.9.tar.gz
sir-0.9/
...
sir-0.9/variables/views.py
[dbarroso@peer00 sir]$ cd sir-0.9/
[dbarroso@peer00 sir-0.9]$ sudo ip netns exec ns-mgmtVRF pip install -r requirements.txt
Downloading/unpacking flask (from -r requirements.txt (line 1))
  Downloading Flask-0.10.1.tar.gz (544kB): 544kB downloaded
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
Downloading/unpacking ipaddress (from -r requirements.txt (line 2))
  Downloading ipaddress-1.0.14-py27-none-any.whl
Downloading/unpacking Werkzeug>=0.7 (from flask->-r requirements.txt (line 1))
  Downloading Werkzeug-0.10.4-py2.py3-none-any.whl (293kB): 293kB downloaded
Downloading/unpacking Jinja2>=2.4 (from flask->-r requirements.txt (line 1))
  Downloading Jinja2-2.8-py2.py3-none-any.whl (263kB): 263kB downloaded
Downloading/unpacking itsdangerous>=0.21 (from flask->-r requirements.txt (line 1))
  Downloading itsdangerous-0.24.tar.gz (46kB): 46kB downloaded
  Running setup.py (path:/tmp/pip_build_root/itsdangerous/setup.py) egg_info for package itsdangerous

    warning: no previously-included files matching '*' found under directory 'docs/_build'
Downloading/unpacking MarkupSafe (from Jinja2>=2.4->flask->-r requirements.txt (line 1))
  Downloading MarkupSafe-0.23.tar.gz
  Running setup.py (path:/tmp/pip_build_root/MarkupSafe/setup.py) egg_info for package MarkupSafe

Installing collected packages: flask, ipaddress, Werkzeug, Jinja2, itsdangerous, MarkupSafe
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
Successfully installed flask ipaddress Werkzeug Jinja2 itsdangerous MarkupSafe
Cleaning up...
