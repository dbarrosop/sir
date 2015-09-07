.. _Deploying SIR Automatically:

Deploying SIR Automatically
===========================

If you want, you can deploy SIR automatically. If you prefer to do it manually go to the section
:ref:`Deploying SIR Manually`.

Requirements
------------

SIR will use the same HTTP and application server than EOS' eAPI so make sure it's running.

Extensions
----------

To install SIR and all of its dependencies automatically we are going to use EOS extensions (SWIX packages). This
will allow us to deploy all the files and do some post-install operations like reconfigure the HTTP/application servers,
start pmacct, initialize the database, etc. Everything is done automatically so sit back and enjoy : )

First, let's get the extensions (make sure you are getting the latest versions, check the releases in the github page)::

    # Get into the management VRF if needed
    peer00.lab#routing-context vrf mgmtVRF
    peer00.lab(vrf:mgmtVRF)#copy https://github.com/dbarrosop/sir/releases/download/v0.17/sir-0.17-1.noarch.swix extension:
    Copy completed successfully.
    peer00.lab(vrf:mgmtVRF)#copy https://github.com/dbarrosop/sir/releases/download/v0.17/pmacct_sir-0.1-1.noarch.swix extension:
    Copy completed successfully.

Now we just have to install the extensions::

    peer00.lab(vrf:mgmtVRF)#extension sir-0.17-1.noarch.swix
    peer00.lab(vrf:mgmtVRF)#extension pmacct_sir-0.1-1.noarch.swix
    peer00.lab(vrf:mgmtVRF)#show extensions
    Name                                       Version/Release           Status extension
    ------------------------------------------ ------------------------- ------ ----
    pmacct_sir-0.1-1.noarch.swix               0.1/1                     A, I      1
    sir-0.17-1.noarch.swix                     0.17/1                    A, I      1

    A: available | NA: not available | I: installed | NI: not installed | F: forced

And that's it!

.. warning:: If you reboot your switch the changes will be lost. To make them permanent execute ``copy installed-extensions boot-extensions``
