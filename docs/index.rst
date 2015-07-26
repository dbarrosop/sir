.. SDN Internet Router (sir) documentation master file, created by
   sphinx-quickstart on Sun Nov 30 09:34:06 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SDN Internet Router (sir)
=========================

The SDN Internet Router, abbreviated SIR, is an agent that you can add to your router. The agent exposes information
that your router can't expose by itself like the BGP table, traffic per BGP prefix or traffic per ASN. This data
is provided both via a WebUI and an API to access this data.

The agent is vendor agnostic as it gathers data using both BGP and netflow/sflow/ipfix. This means it can be attached
to any router or switch that supports those protocols.


.. toctree::
  :maxdepth: 2

  features/index
  architecture/index
  api/api_v1.0
  use_cases/index
  how_to_asr/index
  how_to_eos/index
