Error code reference
====================

When pyx12 validates an X12 document, every problem it finds is recorded
against the document tree at one of five levels (interchange, functional
group, transaction set, segment, or element) with a short numeric code.
The codes match the **AK3 / AK4 / AK5 / AK9 / TA1** "note codes" defined
by the X12 standard for the 997 (4010) and 999 (5010) acknowledgements
that pyx12 emits.

This page documents every code pyx12 produces, what each one means, and
where in the source it is raised. It is intended for developers reading
validator output (CLI or Python API) who need to map a cryptic
``seg_error '5'`` back to a concrete cause in the input file.

How errors are surfaced
-----------------------

The top-level validator (``x12valid`` / :func:`pyx12.x12n_document.x12n_document`)
returns ``False`` when any error fires, writes a 997 / 999 acknowledgement,
and logs the human-readable message. ``x12n_document`` constructs its own
internal error handler and renders results into the 997 / 999 / HTML output
files; for programmatic access to individual errors, drop one level lower to
:class:`pyx12.x12file.X12Reader` or :class:`pyx12.x12context.X12ContextReader`
and supply your own handler. ``errh_list`` collects errors into per-level
lists you can iterate directly.

The five levels:

==================  ====================  ====================
Level               Pyx12 method          997 / 999 segment
==================  ====================  ====================
Interchange (ISA)   ``isa_error``         TA1 (interchange ack)
Functional Group    ``gs_error``          AK9
Transaction Set     ``st_error``          AK5 / IK5
Segment             ``seg_error``         AK3 / IK3
Element / sub-ele   ``ele_error``         AK4 / IK4
==================  ====================  ====================

Element-level codes (AK4 / IK4)
-------------------------------

Raised by :class:`pyx12.map_if.element_if` and :class:`pyx12.map_if.composite_if`
when validating a single element or composite against its map definition.

==========  ==================================================
Code        Meaning
==========  ==================================================
``'1'``     Mandatory data element missing
``'2'``     Conditional element missing (composite: "at least one component required";
            also raised on syntax-rule failures other than mutual exclusion)
``'3'``     Too many data elements in a segment, or too many sub-elements in a composite
``'4'``     Data element too short (length below ``min_len``)
``'5'``     Data element too long (length above ``max_len``); also: composite marked
            as Not Used but populated
``'6'``     Invalid character in data element (charset violation, control characters,
            unnecessary trailing spaces, or non-composite passed where composite expected)
``'7'``     Invalid code value (not a member of the element's valid-code list, external
            code list, or its regex did not match)
``'8'``     Invalid date (DT / D8 / D6 / RD8 type but value is not a valid date)
``'9'``     Invalid time (TM type but value is not a valid time)
``'10'``    Element marked as Not Used but populated; also: syntax-rule type ``E``
            (mutually exclusive elements) violation
==========  ==================================================

Source: see ``element_if.is_valid`` and ``composite_if.is_valid`` in
:doc:`api/pyx12/map_if/index`.

Segment-level codes (AK3 / IK3)
-------------------------------

Raised primarily by :mod:`pyx12.map_walker` while walking the implementation
guide tree, and by :mod:`pyx12.x12file` for low-level structural problems.

==========  ==================================================
Code        Meaning
==========  ==================================================
``'1'``     Segment not found (no map node matched), or segment had a leading space,
            or the segment identifier itself is malformed
``'2'``     Segment found but marked as Not Used in the implementation guide
``'3'``     Mandatory segment is missing where the map required one
``'4'``     Loop occurs more times than the map allows (loop max-repeat exceeded)
``'5'``     Segment occurs more times than the map allows (segment max-repeat exceeded)
``'8'``     Empty segment (no elements)
==========  ==================================================

In addition, :mod:`pyx12.x12file` emits a few **non-numeric** segment codes
for transaction-specific structural checks. These are passed through unchanged
to the acknowledgement and are useful when you need to disambiguate which
counting check failed:

==========  ==================================================
Code        Meaning
==========  ==================================================
``'HL1'``   ``HL01`` value does not match pyx12's running HL count
``'HL2'``   ``HL02`` (parent HL) is not a valid parent in the current HL stack
``'LX'``    837 ``2400/LX01`` service-line number does not match pyx12's count
``'SEG1'``  Segment contains a trailing element terminator (e.g. ``NM1*82*1*~``)
==========  ==================================================

Source: ``walk_tree`` in :doc:`api/pyx12/map_walker/index`, and
``X12Reader._parse_segment`` / ``__iter__`` in :doc:`api/pyx12/x12file/index`.

Transaction-set codes (AK5 / IK5)
---------------------------------

Raised when validating ST/SE envelope structure.

==========  ==================================================
Code        Meaning
==========  ==================================================
``'2'``     Mandatory ``SE`` (Transaction Set Trailer) segment missing at EOF
``'3'``     ``SE02`` does not match the matching ``ST02`` (control-number mismatch)
``'4'``     ``SE01`` count of segments inside the transaction set is wrong
``'23'``    ``ST02`` transaction set control number is not unique within the file
==========  ==================================================

Functional-group codes (AK9)
----------------------------

Raised when validating GS/GE envelope structure.

==========  ==================================================
Code        Meaning
==========  ==================================================
``'3'``     Unterminated GS loop / mandatory ``GE`` missing
``'4'``     ``GE02`` does not match the matching ``GS06``
``'5'``     ``GE01`` count of transaction sets in the group is wrong
``'6'``     ``GS06`` group control number is not unique within the file
==========  ==================================================

Interchange codes (TA1)
-----------------------

Raised when validating ISA/IEA envelope structure. These three-digit codes
match the values defined for the ``TA105`` element of a TA1 interchange
acknowledgement.

==========  ==================================================
Code        Meaning
==========  ==================================================
``'001'``   ``IEA02`` does not match the matching ``ISA13``
``'021'``   ``IEA01`` count of functional groups in the interchange is wrong
``'023'``   Mandatory ``IEA`` (Interchange Control Trailer) missing at EOF
``'024'``   Unterminated GS loop within the interchange
``'025'``   ``ISA13`` interchange control number is not unique within the file
==========  ==================================================

Source: ``X12Reader._parse_segment`` and ``X12Reader.cleanup`` in
:doc:`api/pyx12/x12file/index`.

Worked example: ``seg_error '5'``
---------------------------------

Suppose ``x12valid`` produces this output against an 837P:

.. code-block:: text

   ERROR: Segment NM1 exceeded max count.  Found 2, should have 1
       (line 142, code='5')

This is a **segment-level** error (because the method was ``seg_error``),
code ``'5'`` (segment max-repeat exceeded). Looking up code ``'5'`` in
the segment table above tells you the loop is allowing the ``NM1`` to
appear more times than the implementation guide permits — typically a
sign that two distinct loop instances have been collapsed into one
because of a missing loop-anchor segment between them.

To debug:

1. Open the input at line 142.
2. Walk backwards to the previous loop-anchor segment (often ``HL`` or ``CLM``).
3. Check whether a required separator segment (``CLM``, ``LX``, ``HL``, …)
   is missing — that is usually why the second occurrence of ``NM1`` is
   being attached to the previous loop instead of starting a new one.

Reading errors from Python
--------------------------

For programmatic access, validate via :class:`pyx12.x12context.X12ContextReader`
with an :class:`pyx12.error_handler.errh_list` so each level's errors land in
plain lists you can iterate:

.. code-block:: python

   import pyx12.error_handler
   import pyx12.params
   import pyx12.x12context

   param = pyx12.params.params()
   errh = pyx12.error_handler.errh_list()

   with open("claim.x12", "rb") as fd_in:
       src = pyx12.x12context.X12ContextReader(param, errh, fd_in)
       for _ in src.iter_segments():
           pass  # walking the document populates errh

   for code, msg in errh.err_isa:
       print(f"ISA  {code}: {msg}")
   for code, msg in errh.err_gs:
       print(f"GS   {code}: {msg}")
   for code, msg in errh.err_st:
       print(f"ST   {code}: {msg}")
   for code, msg, value in errh.err_seg:
       print(f"SEG  {code}: {msg} (value={value!r})")
   for code, msg, value, ref_des in errh.err_ele:
       print(f"ELE  {code} ({ref_des}): {msg} (value={value!r})")

For the tree-shaped handler that the 997 / 999 generators consume, use
:class:`pyx12.error_handler.err_handler` and walk it with the
:class:`pyx12.error_visitor.error_visitor` protocol — see
:class:`pyx12.error_debug.error_debug_visitor` for a worked example.
