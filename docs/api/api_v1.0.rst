**********************
API v1.0 Documentation
**********************

###
API
###

Variables
*********

When reading this documentation you will find variables in two forms:

* **<variable>**: Variables that are between ``<>`` have to be replaced by their values in the URL. For example, ``/api/v1.0/variables/categories/<category>`` will turn into ``/api/v1.0/variables/categories/my_category``.
* **variable**: Variables that are NOT enclosed by ``<>``:
 * If the method is a GET variables that are between ``<>`` have to be replaced by their values in the URL. For example, ``/api/v1.0/variables/categories/<category>`` will turn into ``/api/v1.0/variables/categories/my_category``.
 * If the method is a POST or a PUT variables variables that are between ``<>`` have to be sent as a JSON object.

Responses
*********

All the responses from the agent will be in JSON format and will include three sections:

* **meta**: Meta information about the response. For example, *request_time*, *length* of the response or if there was any *error*.
* **parameters**: The parameters used for the call.
* **result**: The result of the call or a description of the error if there was any.

For example, for the following call::

    /api/v1.0/analytics/top_prefixes?limit_prefixes=10&start_time=2015-07-13T14:00&end_time=2015-07-14T14:00&net_masks=20,24

You will get the following response:

.. code-block:: json
    :linenos:

    {
      "meta": {
        "error": false,
        "length": 10,
        "request_time": 11.99163
      },
      "parameters": {
        "end_time": "2015-07-14T14:00",
        "exclude_net_masks": false,
        "limit_prefixes": 10,
        "net_masks": "20,24",
        "start_time": "2015-07-13T14:00"
      },
      "result": [
        {
          "as_dst": 43650,
          "key": "194.14.177.0/24",
          "sum_bytes": 650537594
        },
        ...
        {
          "as_dst": 197301,
          "key": "80.71.128.0/20",
          "sum_bytes": 5106731
        }
      ]
    }

#########
Endpoints
#########

Analytics Endpoint
******************

/api/v1.0/analytics/top_prefixes
================================

GET
---

Description
___________

Retrieves TOP prefixes sorted by the amount of bytes that they consumed during the specified period of time.

Arguments
_________

* **start_time**: Mandatory. Datetime in unicode string following the format ``%Y-%m-%dT%H:%M:%S``. Starting time of the range.
* **end_time**: Mandatory. Datetime in unicode string following the format ``%Y-%m-%dT%H:%M:%S``. Ending time of the range.
* **limit_prefixes**: Optional. Number of top prefixes to retrieve.
* **net_masks**: Optional. List of prefix lengths to filter in or out.
* **exclude_net_masks**: Optional. If set to any value it will return prefixes with a prefix length not included in net_masks. If set to 0 it will return only prefixes with a prefix length included in net_masks. Default is 0.

Returns
_______

A list of prefixes sorted by sum_bytes. The attribute sum_bytes is the amount of bytes consumed during the specified time.

Examples
--------

::

    http://127.0.0.1:5000/api/v1.0/analytics/top_prefixes?limit_prefixes=10&start_time=2015-07-13T14:00&end_time=2015-07-14T14:00
    http://127.0.0.1:5000/api/v1.0/analytics/top_prefixes?limit_prefixes=10&start_time=2015-07-13T14:00&end_time=2015-07-14T14:00&net_masks=20,24
    http://127.0.0.1:5000/api/v1.0/analytics/top_prefixes?limit_prefixes=10&start_time=2015-07-13T14:00&end_time=2015-07-14T14:00&net_masks=20,24&exclude_net_masks=1


/api/v1.0/analytics/top_asns
============================

GET
---

Description
___________

Retrieves TOP ASN's sorted by the amount of bytes that they consumed during the specified period of time.

Arguments
_________

* **start_time**: Mandatory. Datetime in unicode string following the format ``%Y-%m-%dT%H:%M:%S``. Starting time of the range.
* **end_time**: Mandatory. Datetime in unicode string following the format ``%Y-%m-%dT%H:%M:%S``. Ending time of the range.

Returns
_______

A list of ASN's sorted by sum_bytes. The attribute sum_bytes is the amount of bytes consumed during the specified time.

Examples
--------

::

    http://127.0.0.1:5000/api/v1.0/analytics/top_asns?start_time=2015-07-13T14:00&end_time=2015-07-14T14:00

Variables Endpoint
******************

/api/v1.0/variables
===================

GET
---

Description
___________

Retrieves all the variables in the system.

Arguments
_________

Returns
_______

A list of all the variables.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables

POST
----

Description
___________

You can create a variable from the CLI with curl like this:

::

    curl -i -H "Content-Type: application/json" -X POST -d '{"name": "test_var", "content": "whatever", "category": "development", "extra_vars": {"ads": "qwe", "asd": "zxc"}}' http://127.0.0.1:5000/api/v1.0/variables

Arguments
_________

* **content**: Content of the variable.
* **category**: Category of the variable.
* **name**: Name of the variable.
* **extra_vars**: Use this field to add extra data to your variable. It is recommended to use a JSON string.

Returns
_______

The variable that was just created.

Examples
________

/api/v1.0/variables/categories
==============================

GET
---

Description
___________

Retrieves all the categories in the system.

Arguments
_________

Returns
_______

A list of all the categories.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables/categories

/api/v1.0/variables/categories/<category>
=========================================

GET
---

Description
___________

Retrieves all the variables the belong to <category> in the system.

Arguments
_________

* **<category>**: Category you want to query.

Returns
_______

A list of variables belonging to <category>.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables/categories/<category>

/api/v1.0/variables/categories/<category>/<name>
================================================

GET
---

Description
___________

Retrieves the variable with <name> and <category>.

Arguments
_________

* **<category>**: Category of the variable you want to retrieve.
* **<name>**: Name of the variable you want to retrieve.

Returns
_______

A list of variables belonging to <category>.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables/categories/<category>/<name>

PUT
---

Description
___________

This API call allows you to modify all of some of the values of a variable. For example, you can update the name and the extra_vars of a variable with the following command:

.. code-block:: json
    :linenos:

     curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "test_varc", "extra_vars": "{'my_param1': 'my_value1', 'my_param2': 'my_value2'}"}' http://127.0.0.1:5000/api/v1.0/variables/categories/development/test_vara HTTP/1.0 200 OK Content-Type: application/json Content-Length: 358 Server: Werkzeug/0.10.4 Python/2.7.8 Date: Tue, 21 Jul 2015 10:16:22 GMT
     {
      "meta": {
        "error": false,
        "length": 1,
        "request_time": 0.0055
      },
      "parameters": {
        "categories": "development",
        "name": "test_vara"
      },
      "result": [
        {
          "category": "development",
          "content": "whatever",
          "extra_vars": "{my_param1: my_value1, my_param2: my_value2}",
          "name": "test_varc"
        }
      ]
      }

Arguments
_________

* **category**: Optional. New category.
* **content**: Optional. New content.
* **name**: Optional. New name.
* **<name>**: Name of the variable you want to modify.
* **<category>**: Category of the variable you want to modify.
* **extra_vars**: Optional. New extra_vars.

Returns
_______

The variable with the new data.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables/categories/<category>/<name>

DELETE
------

Description
___________

Deletes a variable. For example:

.. code-block:: html
    :linenos:

     curl -i -X DELETE http://127.0.0.1:5000/api/v1.0/variables/categories/deveopment/test_vara HTTP/1.0 200 OK Content-Type: application/json Content-Length: 183 Server: Werkzeug/0.10.4 Python/2.7.8 Date: Tue, 21 Jul 2015 10:17:27 GMT
     {
      "meta": {
        "error": false,
        "length": 0,
        "request_time": 0.0016
      },
      "parameters": {
        "categories": "deveopment",
        "name": "test_vara"
      },
      "result": []
     }

Arguments
_________

* **<category>**: Category of the variable you want to delete.
* **<name>**: Name of the variable you want to delete.

Returns
_______

An empty list.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables/categories/<category>/<name>

Pmacct Endpoint
***************

/api/v1.0/pmacct/dates
======================

GET
---

Description
___________

Retrieves all the available dates in the system.

Arguments
_________

Returns
_______

A list of all the available dates in the system.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/pmacct/dates

/api/v1.0/pmacct/flows
======================

GET
---

Description
___________

Retrieves all the available dates in the system.

Arguments
_________

* **start_time**: Mandatory. Datetime in unicode string following the format ``'%Y-%m-%dT%H:%M:%S'``. Starting time of the range.
* **end_time**: Mandatory. Datetime in unicode string following the format ``'%Y-%m-%dT%H:%M:%S'``. Ending time of the range.

Returns
_______

A list of all the available dates in the system.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/pmacct/flows?limit_prefixes=10&start_time=2015-07-14T14:00&end_time=2015-07-14T14:01
    http://127.0.0.1:5000/api/v1.0/pmacct/flows?limit_prefixes=10&start_time=2015-07-13T14:00&end_time=2015-07-14T14:00

/api/v1.0/pmacct/bgp_prefixes
=============================

GET
---

Description
___________

Retrieves all the BGP prefixes in the system.

.. warning:: Do it only if need it. If you have the full feed this can return hundreds of MB of data.

Arguments
_________

* **date**: Mandatory. Datetime in unicode string following the format ``'%Y-%m-%dT%H:%M:%S'``.

Returns
_______

A list of all the available BGP prefixes in the system.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/pmacct/bgp_prefixes?date=2015-07-16T11:00:01
