API Reference
=============

The pyx12 public API is organized into the following thematic groups.
For an exhaustive auto-generated tree of every module, attribute, and
class, see the full :doc:`api/pyx12/index`.

Reading and writing X12
-----------------------

- :doc:`api/pyx12/x12file/index` — streaming reader/writer for an X12 data stream
- :doc:`api/pyx12/x12context/index` — context-aware parser; iterate claim loops, alter children, track state
- :doc:`api/pyx12/rawx12file/index` — low-level interface to an X12 input stream

Segments and paths
------------------

- :doc:`api/pyx12/segment/index` — segment, composite, and element model
- :doc:`api/pyx12/path/index` — X12 path parser (XPath-style references into a transaction)

Validation
----------

- :doc:`api/pyx12/validation/index` — data element type validation (numeric, ID, AN, DT, TM, …)
- :doc:`api/pyx12/codes/index` — external code list lookup (place-of-service, claim status, …)
- :doc:`api/pyx12/dataele/index` — normalized data element catalog

Map interface
-------------

- :doc:`api/pyx12/map_if/index` — load and traverse an X12N implementation guide map
- :doc:`api/pyx12/map_index/index` — locate the correct map XML for a given transaction
- :doc:`api/pyx12/map_walker/index` — walk a map tree to find the node matching the next segment

XML rendering
-------------

- :doc:`api/pyx12/x12xml/index` — XML rendering of an X12 document
- :doc:`api/pyx12/x12xml_simple/index` — simpler XML output format
- :doc:`api/pyx12/xmlx12_simple/index` — round-trip XML (simple form) back into X12
- :doc:`api/pyx12/xmlwriter/index` — minimal XML output helper

Errors and reporting
--------------------

- :doc:`api/pyx12/errors/index` — exception classes
- :doc:`api/pyx12/error_handler/index` — error tree, attaches errors to the ISA/GS/ST hierarchy
- :doc:`api/pyx12/error_html/index` — HTML rendering of validation errors

Top-level driver
----------------

- :doc:`api/pyx12/x12n_document/index` — high-level entry point: validate and emit 997/999/HTML/XML
- :doc:`api/pyx12/x12metadata/index` — extract interchange / functional group / transaction metadata
- :doc:`api/pyx12/params/index` — runtime parameters and config-file loading

.. toctree::
   :hidden:
   :maxdepth: 4

   api/pyx12/index
