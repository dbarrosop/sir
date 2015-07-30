=======
Logging
=======

Both SIR and pmacct write logs into files:

* pmacct - ``/var/log/pmacct.log``
* sir - ``/var/log/sir.uwsgi.log``

Just access the files using common linux tools like ``tail` or ``less``::

    lab#bash sudo tail /var/log/sir.uwsgi.log
    *** Operational MODE: single process ***
    added /usr/lib/python2.7/site-packages/ to pythonpath.
    WSGI app 0 (mountpoint='') ready in 1 seconds on interpreter 0xf8463420 pid: 5702 (default app)
    *** uWSGI is running in multiple interpreter mode ***
    spawned uWSGI worker 1 (and the only) (pid: 5702, cores: 1)
    [pid: 5702|app: 0|req: 1/1] ::ffff:10.210.20.240 () {44 vars in 713 bytes} [Wed Jul 29 12:25:20 2015] GET /sir/ => generated 699 bytes in 45 msecs (HTTP/1.1 200) 2 headers in 80 bytes (1 switches on core 0)
    [pid: 5702|app: 0|req: 2/2] ::ffff:10.210.20.240 () {44 vars in 695 bytes} [Wed Jul 29 12:25:20 2015] GET /sir/static/style.css => generated 1862 bytes in 7 msecs via sendfile() (HTTP/1.1 200) 7 headers in 284 bytes (0 switches on core 0)
    [pid: 5702|app: 0|req: 3/3] ::ffff:10.210.20.240 () {44 vars in 733 bytes} [Wed Jul 29 12:25:20 2015] GET /sir/static/highlight_styles/default.css => generated 2644 bytes in 2 msecs via sendfile() (HTTP/1.1 200) 7 headers in 285 bytes (0 switches on core 0)
    [pid: 5702|app: 0|req: 4/4] ::ffff:10.210.20.240 () {44 vars in 696 bytes} [Wed Jul 29 12:25:20 2015] GET /sir/static/highlight.pack.js => generated 9057 bytes in 2 msecs via sendfile() (HTTP/1.1 200) 7 headers in 286 bytes (0 switches on core 0)
    [pid: 5702|app: 0|req: 5/5] ::ffff:10.210.20.240 () {44 vars in 694 bytes} [Wed Jul 29 12:25:20 2015] GET /sir/static/scripts/Chart.js => generated 109610 bytes in 2 msecs via sendfile() (HTTP/1.1 200) 7 headers in 290 bytes (0 switches on core 0)
