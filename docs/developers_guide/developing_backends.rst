*******************
Developing Backends
*******************

If you want to develop your own Backend plugin the easiest way to do it is:

   #. Create a new file and a new class inheriting from the class :py:class:`~bgp_controller.backend.base.Backend`
   #. Override all the methods inherited from the parent class with the exception of __init__
   #. Implement your own code respecting the input and the output of its methods.

Configuration Options
=====================

If you need to add configuration variables for your backend like connection string, username, password,
or others, you can specify them in the configuration file inside the 'backend_options' dictionary. For example::

    backend_options:
        sqlite_file: '/workspace/pmacct_data/output/flows/pmacct.db' # Path to the SQLite database
        retention: 7                                                 # Days to hold old data.

You will be able to access those variables as 'self.conf[variable_name]'. For example::

    >>> print self.conf['retention']
    7

Documenting the backend
=======================

If you are writing a backend, please, follow this convention when documenting it::

    Name:
        Name of the plugin
    Author:
        Author's Name <Author's email>
    Description:
        Description of the backend
    Configuration:
        A list containing which configuration parameters are required and why.

Backend
=======

Below you can find the base :py:class:`~bgp_controller.backend.base.Backend` you have to inherit from. You can see all
the methods you have to implement, their input and their output.

.. autoclass:: bgp_controller.backend.base.Backend
    :members:
    :undoc-members:
    :show-inheritance:
