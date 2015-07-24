#########
Variables
#########

Variables
---------

You can store in the agent and retrieve later any arbitrary data that you want. This is useful if you plan to write
applications that consumes data via the API to perform some actions. For example, in the example below you can see
a variable called ``fib_optimizer``. The data in the content is the actual configuration for that application. The
application will retrieve the Top N prefixes via the API and install them in a commodity switch. Thanks to these
feature we can tweak the behavior of that application from a centralized management tool while allowing the device
to run independently.

Use this in any way you want. This will not influence how the agent performs. It's just a convenient way for you
to store/retrieve some data for some applications that you might be running using the SIR API.

.. image:: variables.png
    :align: center
    :alt: variables
