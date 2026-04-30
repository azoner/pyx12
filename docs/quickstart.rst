Quickstart
==========

Install
-------

.. code-block:: bash

   uv pip install pyx12

pyx12 has a single runtime dependency (``defusedxml``) and supports
Python 3.11+.

Validate an X12 file from the command line
------------------------------------------

The package installs a handful of console scripts. The most common one is
``x12valid``:

.. code-block:: bash

   x12valid path/to/claim.x12

Errors are reported to stderr; pass ``-H`` to also write an HTML view of the
document next to the input file. See :doc:`cli` for the full set of CLI
tools and their options.

Validate an X12 file from Python
--------------------------------

The high-level entry point is :func:`pyx12.x12n_document.x12n_document`. It
takes an input stream, validates it, and writes a 997 or 999 acknowledgement
to the output stream.

.. code-block:: python

   import sys
   import pyx12.error_handler
   import pyx12.params
   import pyx12.x12n_document

   param = pyx12.params.params()
   errh = pyx12.error_handler.errh_null()

   with open("claim.x12", "rb") as fd_in, open("ack.997", "w") as fd_997:
       result = pyx12.x12n_document.x12n_document(
           param=param,
           src_file=fd_in,
           fd_997=fd_997,
           fd_html=None,
           fd_xmldoc=None,
           xslt_files=None,
       )

   sys.exit(0 if result else 1)

Iterate claim loops with X12ContextReader
-----------------------------------------

For programmatic access to the parsed document, use
:class:`pyx12.x12context.X12ContextReader`. The example below walks every
``2300`` claim loop in an 837 and patches an ``SV1`` element on each
``2400`` service line:

.. code-block:: python

   import pyx12.error_handler
   import pyx12.params
   import pyx12.x12context

   param = pyx12.params.params()
   errh = pyx12.error_handler.errh_null()

   with open("837.x12", "rb") as fd_in:
       src = pyx12.x12context.X12ContextReader(param, errh, fd_in)
       for datatree in src.iter_segments("2300"):
           for loop2400 in datatree.select("2400"):
               print(loop2400.get_value("SV101"))
               loop2400.set_value("SV102", "xx")
               if loop2400.exists("PWK"):
                   loop2400.delete("PWK")
           for seg_node in datatree.iterate_segments():
               print(seg_node.format())

What's next
-----------

* :doc:`cli` — every console script with its options.
* :doc:`api` — full module-level API reference.
