SDN Internet Router (sir)
=========================

The SDN Internet Router, abbreviated SIR, is an agent that you can add to your router. The agent exposes information that your router can't expose by itself like the BGP table, traffic per BGP prefix or traffic per ASN. This data is then provided both via a WebUI and an API.

The agent is vendor agnostic as it gathers data using both BGP and netflow/sflow/ipfix. This means it can be attached to any router or switch that supports those protocols.

Features
========

The agent will expose a Web UI and an API that will allow you do things like:

* Retrieve Top ASN's based in bandwidth usage.
* Retrieve Top prefixes based in bandwidth usage.
* Simulate what would happen if you had top N prefixes only in your FIB instead of the full routing table.
* Store and retrieve arbitrary data.
* Get raw BGP from your router.
* Get raw flow data from your router.
* Look for all the prefixes that traverses or originates in a particular ASN.
* Check all the prefixes in the router that allows you to reach certain prefixes or IP.

You can read the full list of features in the following [link](http://sdn-internet-router-sir.readthedocs.org/en/latest/features/index.html).

Applications
============

This agent will give you some visibility about your network. You can use this data to better choose your network equipment, to do traffic engineering, capacity planning, peering decisions... anything you want. You can see some use cases in the following [link](http://sdn-internet-router-sir.readthedocs.org/en/latest/use_cases/index.html).

Here is a list of links where you can get tools that leverages on SIR:

* [pySIR](https://github.com/dbarrosop/pySIR) - This is a python API that helps you interact with the API. It implements all the API calls that the API supports. It's just a convenient of coding without taking care of the requests or having to handle errors.
* [sir_tools](https://github.com/dbarrosop/sir_tools) - A collection of tools that takes advantage of SIR API to perform several operations.

Documentation
=============

You can find the documentation on [Read the Docs](http://sdn-internet-router-sir.readthedocs.org/en/latest/).
