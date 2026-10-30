Error code reference
====================

When pyx12 validates an X12 document, every problem it finds is recorded
against the document tree at one of five levels (interchange, functional
group, transaction set, segment, or element).

pyx12 4.1.0 introduced an internal **pyx12 error code namespace**
(``ELE_6_invalid_composite``, ``SEG_3_too_many_elements``, …) backed by
a central registry in :mod:`pyx12.error_codes`. Producers (validators,
walker, parser) emit pyx12 codes; visitors translate to the X12-spec
**AK3 / AK4 / AK5 / AK9 / TA1** "note codes" at output time. The pyx12
codes appear in:

- the ``err_cde`` field on :class:`pyx12.error_item.EleError` /
  :class:`pyx12.error_item.SegError`,
- the ``err_cde`` field on entries in :class:`pyx12.error_handler.errh_list` /
  the ``err_handler`` tree,
- the ``err_cde`` field on each error in :doc:`JSON output <api/pyx12/errh_json/index>`,
  paired with an ``x12_code`` field carrying the dereferenced X12 code.

The X12 numeric codes ("1", "8", etc.) appear only in the 997 / 999
acknowledgement output and the JSON ``x12_code`` field — visitors look
them up via :data:`pyx12.error_codes.ERROR_CODES`.

This page documents every pyx12 code, what each one means, and the X12
code each maps to. It also documents the X12 spec codes that surface
at envelope levels (ISA / GS / ST) which are not yet migrated to pyx12
codes.

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

Pyx12 error codes
-----------------

Code names follow the convention ``<LEVEL>_<X12_CODE>_<descriptor>``:

- **LEVEL** is one of ``ELE``, ``COMP``, ``SEG`` indicating where the
  error attaches in the err_handler tree (composites surface as
  element-level errors in IK4 / AK4 output).
- **X12_CODE** is the AK4 / IK4 / AK3 / IK3 code the visitor will emit
  for this error in the 997 / 999 ack.
- **descriptor** is a short snake-case discriminator. Multiple pyx12
  codes can map to the same X12 code (e.g. four element-level checks
  all map to AK/IK ``"6"``); the descriptor distinguishes them on the
  CLI and in JSON output.

Element-level pyx12 codes
^^^^^^^^^^^^^^^^^^^^^^^^^

Raised by :class:`pyx12.map_if.element_if` when validating a single
element value against its map definition.

==================================  ====  ====  ============================================================
pyx12 code                          AK4   IK4   Meaning
==================================  ====  ====  ============================================================
``ELE_1_mandatory_missing``         1     1     Mandatory data element missing
``ELE_4_too_short``                 4     4     Data element shorter than ``min_len``
``ELE_5_too_long``                  5     5     Data element longer than ``max_len``
``ELE_6_invalid_composite``         6     6     Composite element used at non-composite position
``ELE_6_trailing_space``            6     6     Trailing space in data element
``ELE_6_control_char``              6     6     Control character in data element
``ELE_6_invalid_type_char``         6     6     Invalid character for declared element data type
``ELE_7_regex_fail``                7     7     Data element does not match required regex pattern
``ELE_7_invalid_code``              7     7     Data element value not in valid code list
``ELE_8_invalid_date``              8     8     Invalid date (declared D8/D6/DT/RD8 type)
``ELE_8_invalid_date_range``        8     8     Invalid date in multi-type validation
``ELE_9_invalid_time``              9     9     Invalid time (declared TM type)
``ELE_9_invalid_time_of_day``       9     9     Invalid time-of-day in multi-type validation
``ELE_I10_NOT_USED``                —     I10   Data element marked Not Used (usage='N') but populated
==================================  ====  ====  ============================================================

Composite-level pyx12 codes
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Raised by :class:`pyx12.map_if.composite_if` when validating a
composite element. Surface as element-level errors in IK4 / AK4 output.

==================================  ====  ====  ============================================================
pyx12 code                          AK4   IK4   Meaning
==================================  ====  ====  ============================================================
``COMP_1_mandatory_missing``        1     1     Mandatory composite element missing
``COMP_3_too_many_subelements``     3     3     Composite has too many sub-elements
``COMP_5_not_used``                 5     5     Composite marked Not Used (usage='N') but populated
==================================  ====  ====  ============================================================

Segment-level pyx12 codes
^^^^^^^^^^^^^^^^^^^^^^^^^

Raised by :class:`pyx12.map_if.segment_if` (validator), :mod:`pyx12.map_walker`
(walker), and :mod:`pyx12.x12file` (parser).

================================================  ====  ====  ============================================================
pyx12 code                                        AK3   IK3   Meaning
================================================  ====  ====  ============================================================
``SEG_3_too_many_elements``                       3     3     Segment has too many elements (validator)
``SEG_3_too_many_subelements``                    3     3     **Deprecated, never emitted; removed in 5.0.** Use ``COMP_3_too_many_subelements``
``SEG_2_syntax_relational``                       2     2     Segment syntax rule (relational) violated
``SEG_10_syntax_exclusive``                       10    10    Segment syntax rule (exclusive) violated
``SEG_1_segment_not_found``                       1     1     Unrecognized segment ID (walker)
``SEG_2_segment_not_used``                        2     2     Segment marked Not Used (usage='N')
``SEG_2_loop_not_used``                           2     2     Loop marked Not Used (usage='N')
``SEG_3_mandatory_segment_missing``               3     3     Mandatory segment missing
``SEG_3_mandatory_loop_missing``                  3     3     Mandatory loop missing
``SEG_4_loop_repeat_exceeded``                    4     4     Loop repeat count exceeded
``SEG_5_segment_repeat_exceeded``                 5     5     Segment repeat count exceeded
``SEG_1_invalid_seg_id``                          1     1     Segment identifier malformed (parser)
``SEG_1_leading_space``                           1     1     Segment line started with leading whitespace
``SEG_8_segment_empty``                           8     8     Segment is empty (parser)
``SEG_8_trailing_terminators``                    8     8     Segment has trailing element terminators
``SEG_8_hl_count_mismatch``                       —     —     ``HL01`` does not match running HL count (filtered from ack)
``SEG_8_hl_invalid_parent``                       —     —     ``HL02`` is not a valid HL parent (filtered from ack)
``SEG_8_lx_count_mismatch``                       —     —     837 ``2400/LX01`` does not match LX count (filtered from ack)
================================================  ====  ====  ============================================================

A dash ("—") in the AK3/IK3 column means the code is preserved in the
err_handler tree and JSON output but suppressed from the X12 ack
(historical behavior preserved across the 4.1.0 refactor).

The seg-level **validator** codes (``SEG_3_too_many_elements``,
``SEG_2_syntax_relational``, ``SEG_10_syntax_exclusive``) plus the composite-level codes flow
through the bridge in :func:`pyx12.map_if._segment.apply_segment_errors`,
which routes seg-level errors via ``errh.seg_error`` with a hardcoded
``"8"`` code (X12 spec correctness); the original AK3/IK3 column above
is the canonical mapping for the pyx12 code itself, but the actual ack
output for these specific codes will show ``"8"`` instead. See
:func:`pyx12.map_if._segment.apply_segment_errors` for the routing logic.

Source: see :class:`pyx12.error_codes.ErrorCodeSpec` and
:data:`pyx12.error_codes.ERROR_CODES`.

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
``'5'``     ``GE01`` count of transaction sets in the group is wrong, or a segment
            sits in the group outside any transaction set (see below)
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
``'024'``   Unterminated GS loop within the interchange, or a segment in the
            interchange outside any functional group (see below)
``'025'``   ``ISA13`` interchange control number is not unique within the file
==========  ==================================================

Source: ``X12Reader._parse_segment`` and ``X12Reader.cleanup`` in
:doc:`api/pyx12/x12file/index`.

Segments outside a transaction set
----------------------------------

A segment with no open transaction set (a functional group with no ``ST``,
a repeated ``SE``, ``GE`` or ``IEA``) cannot be reported in an ``AK3``/``IK3``.
pyx12 reports it on the innermost envelope that is still open:

* **Inside an open functional group:** the group is rejected (``AK9*R``) with
  ``AK905`` code ``5``. No ``AK905`` code describes these faults exactly; in
  `RFI 1339 <https://x12.org/resources/requests-for-interpretation/rfi-1339-997999-error-invalid-st>`_
  X12 recommends code ``5`` for a group-level rejection with no specific code.
* **Otherwise:** the interchange gets ``024`` (``ISA_024_invalid_content``),
  which goes out on the TA1 when ``ISA14`` is ``1``.

A fault inside a group is not reported on the TA1. In
`RFI 2435 <https://x12.org/resources/requests-for-interpretation/rfi-2435-ta1-acknowledgment-status-and-note-code-24>`_
X12 says only the ``ISA`` and ``IEA`` are in the TA1's scope. A sender that
sets ``ISA14`` to ``0`` gets no TA1 at all, so it would otherwise see
``AK9*A`` for a group that was rejected.

Worked example: ``SEG_5_segment_repeat_exceeded``
-------------------------------------------------

Suppose ``x12valid`` produces this output against an 837P:

.. code-block:: text

   ERROR: Segment NM1 exceeded max count.  Found 2, should have 1
       (line 142, code='SEG_5_segment_repeat_exceeded', x12_code='5')

This is a **segment-level** error (the ``SEG_`` prefix). Looking it up
in the segment-level table above tells you the loop is allowing the
``NM1`` to appear more times than the implementation guide permits —
typically a sign that two distinct loop instances have been collapsed
into one because of a missing loop-anchor segment between them.

To debug:

1. Open the input at line 142.
2. Walk backwards to the previous loop-anchor segment (often ``HL`` or ``CLM``).
3. Check whether a required separator segment (``CLM``, ``LX``, ``HL``, …)
   is missing — that is usually why the second occurrence of ``NM1`` is
   being attached to the previous loop instead of starting a new one.

The 999 ack for this error will emit ``IK3*NM1*<seg_count>**5~`` (the
``5`` is from the table's IK3 column; ``x12_code`` in JSON output
matches it).

Reading errors from Python
--------------------------

For programmatic access, validate via :class:`pyx12.x12context.X12ContextReader`
with an :class:`pyx12.error_handler.errh_list` so each level's errors land in
plain lists you can iterate. Segment- and element-level codes are pyx12
codes (``SEG_*`` / ``ELE_*`` / ``COMP_*``); ISA / GS / ST envelope codes
are still raw X12 strings.

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
       print(f"ISA  {code}: {msg}")              # raw X12 codes ("025", "010", ...)
   for code, msg in errh.err_gs:
       print(f"GS   {code}: {msg}")              # raw X12 codes
   for code, msg in errh.err_st:
       print(f"ST   {code}: {msg}")              # raw X12 codes
   for code, msg, value in errh.err_seg:
       print(f"SEG  {code}: {msg}")              # pyx12 codes ("SEG_3_*", ...)
   for code, msg, value, ref_des in errh.err_ele:
       print(f"ELE  {code} ({ref_des}): {msg}")  # pyx12 codes ("ELE_8_*", ...)

For the tree-shaped handler that the 997 / 999 generators consume, use
:class:`pyx12.error_handler.err_handler` and walk it with the
:class:`pyx12.error_visitor.error_visitor` protocol — see
:class:`pyx12.error_debug.error_debug_visitor` for a worked example.

To resolve a pyx12 code to its X12 ack code in your own code, look it
up in the registry:

.. code-block:: python

   from pyx12.error_codes import ERROR_CODES, x12_code_for

   spec = ERROR_CODES["ELE_8_invalid_date"]
   spec.ak_code  # "8" (4010 ack)
   spec.ik_code  # "8" (5010 ack)
   spec.level    # "ELE"
   spec.description  # "Data element contains an invalid date (D8/D6/DT)"

   # `x12_code_for` is the helper used by the JSON visitor's `x12_code`
   # field: returns spec.ik_code (preferred) or spec.ak_code, or the
   # err_cde itself for codes not in ERROR_CODES (envelope-level codes).
   x12_code_for("ELE_8_invalid_date")  # -> "8"
   x12_code_for("025")                 # -> "025" (ISA-level passthrough)

Suppressing codes
-----------------

Pyx12 codes can be filtered out before they reach the err_handler tree.
Suppressed errors do not appear in the 997/999 ack, the JSON output,
or any error-count tally. The validator's overall verdict (valid/invalid)
is unaffected by suppression — pyx12 still knows the segment had errors,
it just doesn't surface them to consumers.

CLI:

.. code-block:: text

   x12valid -J --suppress ELE_6_invalid_composite,SEG_3_too_many_elements -- input.x12

The flag is comma-separated; you can also repeat ``-S`` / ``--suppress``
to add codes:

.. code-block:: text

   x12valid -S ELE_6_invalid_composite -S SEG_3_too_many_elements -- input.x12

Programmatically:

.. code-block:: python

   import pyx12.params
   import pyx12.x12n_document

   param = pyx12.params.params()
   param.set("suppress_error_codes", {"ELE_6_invalid_composite"})

   with open("input.x12") as fd, open("output.997", "w") as fd_997:
       pyx12.x12n_document.x12n_document(param, fd, fd_997, None, None)

Suppression operates on **pyx12 codes**, not the underlying X12 codes:
suppressing ``ELE_6_invalid_composite`` filters only the composite-mistake
emission, not the three other element-level checks that also map to AK4
``"6"`` (control character, trailing space, invalid type character).
This is the granular control the pyx12 code namespace was introduced to
provide.
