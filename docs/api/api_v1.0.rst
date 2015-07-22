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
 * If the method is a GET variables that are between <> have to be replaced by their values in the URL. For example, ``/api/v1.0/variables/categories/<category>`` will turn into ``/api/v1.0/variables/categories/my_category``.
 * If the method is a POST or a PUT variables variables that are between <> have to sent as a JSON object.

Responses
*********

All the responses from the agent will be in JSON format and will include three sections:

* **meta**: Meta information about the response. For example, ***request_time***, ***length*** of the response or if there was any ***error***.
* **parameters**: The parameters used for the call.
* **result**: The result of the call or a description of the error if there was any.

For example, for the following call you will get the following response:

.. code-block:: html
    :linenos:

    /api/v1.0/analytics/top_prefixes?limit_prefixes=10&start_time=2015-07-13T14:00&end_time=2015-07-14T14:00&net_masks=20,24


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

Whatever

POST
----

Whatever

/api/v1.0/analytics/top_prefixes
================================

GET
---

Whatever

POST
----

Whatever
