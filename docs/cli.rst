Command-line tools
==================

Installing the package places the following scripts on ``PATH``. Each section
below shows the live ``--help`` output captured during the docs build.

x12valid
--------

Parse an ANSI X12N data file and validate it against the appropriate HIPAA
implementation guide. Emits errors to stderr; with ``-H`` also writes an
HTML rendering next to the input file.

.. command-output:: x12valid --help

x12norm
-------

Re-format an X12 document. Adds segment-terminator newlines with ``-e`` and
patches common loop / segment counting errors with ``-f``. Reads stdin and
writes stdout when no files are given.

.. command-output:: x12norm --help

x12html
-------

Render an X12 document as an HTML view that highlights structure and errors.

.. command-output:: x12html --help

x12info
-------

Print summary metadata (interchange / functional group / transaction set
counts and identifiers) for an X12 document.

.. command-output:: x12info --help

x12xml
------

Convert an X12 document to its XML representation.

.. command-output:: x12xml --help

xmlx12
------

Convert an XML representation produced by ``x12xml`` back into an X12
document.

.. command-output:: xmlx12 --help
