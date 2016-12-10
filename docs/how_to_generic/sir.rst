==================
Enabling SIR agent
==================

This is super easy to do. First install using pip::

  $ sudo pip install SIR
  You are using pip version 6.0.8, however version 7.1.0 is available.
  You should consider upgrading via the 'pip install --upgrade pip' command.
  Collecting SIR
    Downloading SIR-0.10.tar.gz (79kB)
      100% |################################| 81kB 1.2MB/s
  Collecting flask (from SIR)
    Using cached Flask-0.10.1.tar.gz
  Collecting ipaddress (from SIR)
    Using cached ipaddress-1.0.14-py27-none-any.whl
  Collecting PyYAML (from SIR)
    Using cached PyYAML-3.11.tar.gz
  Collecting Werkzeug>=0.7 (from flask->SIR)
    Using cached Werkzeug-0.10.4-py2.py3-none-any.whl
  Collecting Jinja2>=2.4 (from flask->SIR)
    Downloading Jinja2-2.8-py2.py3-none-any.whl (263kB)
      100% |################################| 266kB 1.1MB/s
  Collecting itsdangerous>=0.21 (from flask->SIR)
    Using cached itsdangerous-0.24.tar.gz
  Collecting MarkupSafe (from Jinja2>=2.4->flask->SIR)
    Using cached MarkupSafe-0.23.tar.gz
  Installing collected packages: MarkupSafe, itsdangerous, Jinja2, Werkzeug, PyYAML, ipaddress, flask, SIR
    Running setup.py install for MarkupSafe
      building 'markupsafe._speedups' extension
      clang -fno-strict-aliasing -fno-common -dynamic -I/usr/local/include -I/usr/local/opt/sqlite/include -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/include/python2.7 -c markupsafe/_speedups.c -o build/temp.macosx-10.10-x86_64-2.7/markupsafe/_speedups.o
      clang -bundle -undefined dynamic_lookup -L/usr/local/lib -L/usr/local/opt/sqlite/lib build/temp.macosx-10.10-x86_64-2.7/markupsafe/_speedups.o -o build/lib.macosx-10.10-x86_64-2.7/markupsafe/_speedups.so
    Running setup.py install for itsdangerous


    Running setup.py install for PyYAML
      checking if libyaml is compilable
      clang -fno-strict-aliasing -fno-common -dynamic -I/usr/local/include -I/usr/local/opt/sqlite/include -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/include/python2.7 -c build/temp.macosx-10.10-x86_64-2.7/check_libyaml.c -o build/temp.macosx-10.10-x86_64-2.7/check_libyaml.o
      build/temp.macosx-10.10-x86_64-2.7/check_libyaml.c:2:10: fatal error: 'yaml.h' file not found
      #include <yaml.h>
               ^
      1 error generated.
      libyaml is not found or a compiler error: forcing --without-libyaml
      (if libyaml is installed correctly, you may need to
       specify the option --include-dirs or uncomment and
       modify the parameter include_dirs in setup.cfg)

    Running setup.py install for flask
    Running setup.py install for SIR
    Successfully installed Jinja2-2.8 MarkupSafe-0.23 PyYAML-3.11 SIR-0.10 Werkzeug-0.10.4 flask-0.10.1 ipaddress-1.0.14 itsdangerous-0.24

Now configure SIR. Edit file ``settings.py``::

    DATABASE = '/pmacct-1.5.1/output/pmacct.db'         # Path to the db
    BGP_FOLDER = '/pmacct-1.5.1/output'         # Path to the folder where BGP info is
    DEBUG = False                                       # Set to True only if you are trying to develop and your environment is completely secure
    SECRET_KEY = 'My_super_duper_secret_key'            # Secret key. Keep it secret.
    BIND_IP = '0.0.0.0'                                 # IP you want to bind the service to
    PORT= 8080                                          # Port you want to bind the service to

.. note:: You can place the ``settings.py`` file anywhere you like. However, you will have to set the environment variable ``SIR_SETTINGS`` pointing towards it so it can be found. For example, ``export SIR_SETTINGS=/path/to/settings.py``.

Now you need an application server like UWSGI or gunicorn to run the application. There is tons of documentation out there
on how to run flask application. I suggest you to start `here <http://flask.pocoo.org/docs/0.10/deploying/>`_. For the
sake of testing we can use gunicorn like this::

    $ sudo pip install gunicorn
    You are using pip version 6.0.8, however version 7.1.0 is available.
    You should consider upgrading via the 'pip install --upgrade pip' command.
    Collecting gunicorn
      Using cached gunicorn-19.3.0-py2.py3-none-any.whl
    Installing collected packages: gunicorn
      Compiling /private/var/folders/d9/9h8nsvsd2_vgt9y1l73jhhvr0000gn/T/pip-build-FcSaUJ/gunicorn/gunicorn/workers/_gaiohttp.py


    Successfully installed gunicorn-19.3.0
    $ sudo gunicorn sir.agent:app
    [2015-07-30 13:21:30 +0200] [46008] [INFO] Starting gunicorn 19.3.0
    [2015-07-30 13:21:30 +0200] [46008] [INFO] Listening at: http://127.0.0.1:8000 (46008)
    [2015-07-30 13:21:30 +0200] [46008] [INFO] Using worker: sync
    [2015-07-30 13:21:30 +0200] [46017] [INFO] Booting worker with pid: 46017

At this point you should be able to access SIR at http://127.0.0.1:8000.
