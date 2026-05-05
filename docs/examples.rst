Examples
========

This page collects worked examples that ship in :mod:`pyx12.examples`.
Each demonstrates a different pattern for working with X12 documents,
ordered roughly from low-level stream handling up to a full transaction-set
to-JSON pipeline. Run any of them directly from a checkout — every script
has a ``__main__`` entry point — or copy the techniques into your own
code.

Splitting on ST loops with X12Reader
------------------------------------

:download:`st_iterator.py <../pyx12/examples/st_iterator.py>` splits an
X12 interchange that contains multiple ST/SE transaction sets into one
X12 file per ST loop. It uses the streaming :class:`pyx12.x12file.X12Reader`
together with :func:`itertools.groupby` to chunk segments by their owning
ST envelope, then writes each chunk through :class:`pyx12.x12file.X12Writer`
which auto-closes the ST / GS / ISA loops on ``Close()``. The example also
shows how to renumber the ISA control number (``ISA13``) and GS group
control number (``GS06``) per output file.

This is the lowest-level approach — useful when you don't need
loop-aware parsing and want to keep memory flat over very large
interchanges.

.. literalinclude:: ../pyx12/examples/st_iterator.py
   :language: python

Splitting on ST loops with X12ContextReader
-------------------------------------------

:download:`st_context_iterator.py <../pyx12/examples/st_context_iterator.py>`
solves the same problem as ``st_iterator.py`` but parses the input
through :class:`pyx12.x12context.X12ContextReader` and its loop-aware
``iter_segments`` interface. Use this style when you also need to inspect
or modify segments inside specific loops (here the 834's ``2000`` member
loops) while you split — the context reader keeps parent / child
relationships and the implementation-guide map node attached to each
yielded ``X12DataNode``.

.. literalinclude:: ../pyx12/examples/st_context_iterator.py
   :language: python

De-identifying an 834 enrollment file
-------------------------------------

:download:`deident834.py <../pyx12/examples/deident834.py>` walks an 834
Benefit Enrollment file and replaces every member's PHI (name, SSN,
Medicaid ID, DOB, address) with synthetic values, writing the rewritten
X12 stream back out. It demonstrates the **mutation pattern**:
:meth:`pyx12.x12context.X12DataNode.set_value` lets you patch element
values on a parsed loop in place, addressed by a path like ``2100A/NM103``
(member last name) or ``REF[0F]02`` (subscriber identifier). Combined
with a ``pyx12.x12file.X12Writer`` you can round-trip a transformed copy
of the input back to disk.

This is a demo and is not production-ready de-identification — the
substitution policy is illustrative only.

.. literalinclude:: ../pyx12/examples/deident834.py
   :language: python

Parsing 834 enrollment into JSON
--------------------------------

:download:`834_x12_json.py <../pyx12/examples/834_x12_json.py>` is a
fuller pipeline: it parses an 834 file and emits one JSON document per
ST transaction set, with the envelope headers, members, providers, and
payers flattened into a structured object. The ``Enrollment834Parser``
class wraps :class:`pyx12.x12context.X12ContextReader`, dispatches on
``datatree.id`` to capture envelope state (ISA / GS / ST / BGN), and
descends into each ``2000`` member loop to extract a member record
along with its nested ``2100A`` (member name), ``2100G`` (responsible
person), ``2300`` (coverage), ``2310`` (provider), and ``2320`` (payer)
loops.

It demonstrates the **transformation pattern**: how to use X12
path expressions like ``2100A/NM109``, ``DTP[356]03``, or
``REF[0F]02`` against a context node to pull values out of a deeply
nested loop without writing per-segment scaffolding, and how to
accumulate the results into nested ``OrderedDict``\\ s suitable for
``json.dumps``.

.. literalinclude:: ../pyx12/examples/834_x12_json.py
   :language: python

Generating a field reference from a sample file
-----------------------------------------------

The next two scripts form a small pipeline that derives a
human-readable field reference for whatever transaction type a sample
X12 file contains. This is useful when you're integrating a new
transaction (or a new vendor's flavor of an existing one) and want to
see exactly which loops, segments, and elements show up — together
with the implementation-guide metadata pyx12 has for each.

:download:`node_iterator.py <../pyx12/examples/node_iterator.py>`
walks the input file with :class:`pyx12.x12file.X12Reader` plus a
:class:`pyx12.map_walker.walk_tree`, manually driving the walker the
same way :func:`pyx12.x12n_document.x12n_document` does internally,
and records every distinct map node it encounters along with its
``base_name``, ``id``, ``name``, ``usage``, ``data_type``, and
length bounds. The result is written to ``node_list.json`` next to
the input file. This is also a worked example of using the map
walker directly, picking the right map via
:class:`pyx12.map_index.map_index`, and switching maps mid-stream
when a 4010 837 reveals its tspc in the BHT segment.

.. literalinclude:: ../pyx12/examples/node_iterator.py
   :language: python

:download:`generate_spec.py <../pyx12/examples/generate_spec.py>`
consumes the ``node_list.json`` and emits two artifacts:

* ``out.csv`` — one row per node with all of the metadata fields,
  suitable for review in a spreadsheet.
* ``map.json`` — element nodes grouped by the section of the
  transaction they belong to (Header, Patient, Claim, ServiceLine,
  ProviderStatus, …), with the section heuristics applied to 277CA
  loop names like ``2200D`` / ``2220D``.  The element list per section
  collapses duplicate ``FormattedName`` collisions by prefixing the
  parent loop name.

.. literalinclude:: ../pyx12/examples/generate_spec.py
   :language: python
