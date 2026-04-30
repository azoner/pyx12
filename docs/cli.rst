Command-line tools
==================

Installing the package places the following scripts on ``PATH``. Each script
is also available as ``python -m pyx12.scripts.<name>``; the ``--help``
output captured below is identical to running the entry-point directly.

x12valid
--------

Parse an ANSI X12N data file and validate it against the appropriate HIPAA
implementation guide. Emits errors to stderr; with ``-H`` also writes an
HTML rendering next to the input file.

.. code-block:: console

   $ x12valid --help

.. literalinclude:: _generated/cli/x12valid.txt
   :language: text

x12norm
-------

Re-format an X12 document. Adds segment-terminator newlines with ``-e`` and
patches common loop / segment counting errors with ``-f``. Reads stdin and
writes stdout when no files are given.

.. code-block:: console

   $ x12norm --help

.. literalinclude:: _generated/cli/x12norm.txt
   :language: text

x12html
-------

Render an X12 document as an HTML view that highlights structure and errors.

.. code-block:: console

   $ x12html --help

.. literalinclude:: _generated/cli/x12html.txt
   :language: text

x12info
-------

Print summary metadata (interchange / functional group / transaction set
counts and identifiers) for an X12 document.

.. code-block:: console

   $ x12info --help

.. literalinclude:: _generated/cli/x12info.txt
   :language: text

x12xml
------

Convert an X12 document to its XML representation.

.. code-block:: console

   $ x12xml --help

.. literalinclude:: _generated/cli/x12xml.txt
   :language: text

xmlx12
------

Convert an XML representation produced by ``x12xml`` back into an X12
document.

.. code-block:: console

   $ xmlx12 --help

.. literalinclude:: _generated/cli/xmlx12.txt
   :language: text
