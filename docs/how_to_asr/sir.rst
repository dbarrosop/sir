==================
Enabling SIR agent
==================

This is super easy to do. First clone SIR and install requirements::

    $ git clone git@github.com:dbarrosop/sir.git
    Cloning into 'sir'...
    remote: Counting objects: 761, done.
    remote: Compressing objects: 100% (154/154), done.
    remote: Total 761 (delta 85), reused 0 (delta 0), pack-reused 599
    Receiving objects: 100% (761/761), 1.84 MiB | 1.25 MiB/s, done.
    Resolving deltas: 100% (373/373), done.
    Checking connectivity... done.
    $ cd sir
    $ pip install -U -r requirements.txt
    /lib/python2.7/site-packages/pip/_vendor/requests/packages/urllib3/util/ssl_.py:90: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
      InsecurePlatformWarning
    Requirement already up-to-date: flask in /lib/python2.7/site-packages (from -r requirements.txt (line 1))
    Requirement already up-to-date: Werkzeug>=0.7 in /lib/python2.7/site-packages (from flask->-r requirements.txt (line 1))
    Requirement already up-to-date: Jinja2>=2.4 in /lib/python2.7/site-packages (from flask->-r requirements.txt (line 1))
    Requirement already up-to-date: itsdangerous>=0.21 in /lib/python2.7/site-packages (from flask->-r requirements.txt (line 1))
    Requirement already up-to-date: markupsafe in /lib/python2.7/site-packages (from Jinja2>=2.4->flask->-r requirements.txt (line 1))

Now configure SIR. Edit file ``settings.py``::

    DATABASE = '/pmacct-1.5.1/output/pmacct.db'         # Path to the db
    BGP_FOLDER = '/spotify/pmacct-1.5.1/output'         # Path to the folder where BGP info is
    DEBUG = False                                       # Set to True only if you are trying to develop and your environment is completely secure
    SECRET_KEY = 'My_super_duper_secret_key'            # Secret key. Keep it secret.
    BIND_IP = '0.0.0.0'                                 # IP you want to bind the service to
    PORT= 8080                                          # Port you want to bind the service to

Finally, start SIR::

    $ sudo python sir.py
