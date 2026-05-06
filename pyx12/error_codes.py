######################################################################
# Copyright
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
pyx12 error code registry.

Producers (validators in pyx12.map_if, the walker in pyx12.map_walker, and
the parser in pyx12.x12file) emit pyx12-internal error codes named
<LEVEL>_<X12_CODE>_<discriminator> (e.g. ELE_6_invalid_composite). Each
code maps to an ErrorCodeSpec in ERROR_CODES, which carries the level,
human-readable description, and the X12 4010 (AK) / 5010 (IK) codes to
emit in 997 / 999 / JSON output.

The table is the single source of truth: visitors look up the pyx12 code
to find the ack-output code, and any future remap (e.g. the historical
"SEG1" parser code routed to AK/IK "8") is a one-line table entry rather
than inline visitor logic.

This is the PR 1 slice — the table is fully populated but no producer
yet emits these codes. Visitors fall back to legacy raw X12-code lookup
when ERROR_CODES.get(err_cde) returns None. Producers migrate
incrementally in PR 2-4; PR 5 drops the legacy fallback.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

LevelT = Literal["ISA", "GS", "ST", "SEG", "ELE"]


@dataclass(frozen=True, slots=True)
class ErrorCodeSpec:
    """Single entry in ERROR_CODES.

    ak_code and ik_code are the X12 acknowledgement codes for 4010 (AK)
    and 5010 (IK) output respectively. None means the code is not
    surfaced in that channel (e.g. parser HL1/HL2/LX bypass the ack
    today; preserve that behavior with both = None).
    """

    code: str
    level: LevelT
    description: str
    ak_code: str | None
    ik_code: str | None


# Element-level pyx12 codes. Module-level constants pair with each
# ERROR_CODES entry for IDE auto-complete and CLI grep-ability.
ELE_1_MANDATORY_MISSING = "ELE_1_mandatory_missing"
ELE_4_TOO_SHORT = "ELE_4_too_short"
ELE_5_TOO_LONG = "ELE_5_too_long"
ELE_6_INVALID_COMPOSITE = "ELE_6_invalid_composite"
ELE_6_TRAILING_SPACE = "ELE_6_trailing_space"
ELE_6_CONTROL_CHAR = "ELE_6_control_char"
ELE_6_INVALID_TYPE_CHAR = "ELE_6_invalid_type_char"
ELE_7_REGEX_FAIL = "ELE_7_regex_fail"
ELE_7_INVALID_CODE = "ELE_7_invalid_code"
ELE_8_INVALID_DATE = "ELE_8_invalid_date"
ELE_8_INVALID_DATE_RANGE = "ELE_8_invalid_date_range"
ELE_9_INVALID_TIME = "ELE_9_invalid_time"
ELE_9_INVALID_TIME_OF_DAY = "ELE_9_invalid_time_of_day"
ELE_10_NOT_USED = "ELE_10_not_used"

# Composite-level pyx12 codes. Composites historically emitted via
# EleError carrying the seg_error code semantics (see _composite.py).
COMP_1_MANDATORY_MISSING = "COMP_1_mandatory_missing"
COMP_3_TOO_MANY_SUBELEMENTS = "COMP_3_too_many_subelements"
COMP_5_NOT_USED = "COMP_5_not_used"

# Segment-level pyx12 codes.
# From _segment.py validators:
SEG_3_TOO_MANY_ELEMENTS = "SEG_3_too_many_elements"
SEG_3_TOO_MANY_SUBELEMENTS = "SEG_3_too_many_subelements"
SEG_2_SYNTAX_RELATIONAL = "SEG_2_syntax_relational"
SEG_10_SYNTAX_EXCLUSIVE = "SEG_10_syntax_exclusive"
# From map_walker.py:
SEG_1_SEGMENT_NOT_FOUND = "SEG_1_segment_not_found"
SEG_2_SEGMENT_NOT_USED = "SEG_2_segment_not_used"
SEG_2_LOOP_NOT_USED = "SEG_2_loop_not_used"
SEG_3_MANDATORY_SEGMENT_MISSING = "SEG_3_mandatory_segment_missing"
SEG_3_MANDATORY_LOOP_MISSING = "SEG_3_mandatory_loop_missing"
SEG_5_SEGMENT_REPEAT_EXCEEDED = "SEG_5_segment_repeat_exceeded"
SEG_4_LOOP_REPEAT_EXCEEDED = "SEG_4_loop_repeat_exceeded"
# From x12file.py parser. SEG1 historically remapped inline to AK/IK "8";
# HL1/HL2/LX historically had no ack remap (filtered out).
SEG_1_INVALID_SEG_ID = "SEG_1_invalid_seg_id"
SEG_1_LEADING_SPACE = "SEG_1_leading_space"
SEG_8_HAS_DATA_ELEMENT_ERRORS = "SEG_8_has_data_element_errors"
SEG_8_SEGMENT_EMPTY = "SEG_8_segment_empty"
SEG_8_TRAILING_TERMINATORS = "SEG_8_trailing_terminators"
SEG_8_HL_COUNT_MISMATCH = "SEG_8_hl_count_mismatch"
SEG_8_HL_INVALID_PARENT = "SEG_8_hl_invalid_parent"
SEG_8_LX_COUNT_MISMATCH = "SEG_8_lx_count_mismatch"


ERROR_CODES: dict[str, ErrorCodeSpec] = {
    # --- Element-level ---
    ELE_1_MANDATORY_MISSING: ErrorCodeSpec(
        code=ELE_1_MANDATORY_MISSING,
        level="ELE",
        description="Mandatory data element missing",
        ak_code="1",
        ik_code="1",
    ),
    ELE_4_TOO_SHORT: ErrorCodeSpec(
        code=ELE_4_TOO_SHORT,
        level="ELE",
        description="Data element too short",
        ak_code="4",
        ik_code="4",
    ),
    ELE_5_TOO_LONG: ErrorCodeSpec(
        code=ELE_5_TOO_LONG,
        level="ELE",
        description="Data element too long",
        ak_code="5",
        ik_code="5",
    ),
    ELE_6_INVALID_COMPOSITE: ErrorCodeSpec(
        code=ELE_6_INVALID_COMPOSITE,
        level="ELE",
        description="Composite element used at non-composite position",
        ak_code="6",
        ik_code="6",
    ),
    ELE_6_TRAILING_SPACE: ErrorCodeSpec(
        code=ELE_6_TRAILING_SPACE,
        level="ELE",
        description="Trailing space in data element",
        ak_code="6",
        ik_code="6",
    ),
    ELE_6_CONTROL_CHAR: ErrorCodeSpec(
        code=ELE_6_CONTROL_CHAR,
        level="ELE",
        description="Control character in data element",
        ak_code="6",
        ik_code="6",
    ),
    ELE_6_INVALID_TYPE_CHAR: ErrorCodeSpec(
        code=ELE_6_INVALID_TYPE_CHAR,
        level="ELE",
        description="Invalid character for declared element data type",
        ak_code="6",
        ik_code="6",
    ),
    ELE_7_REGEX_FAIL: ErrorCodeSpec(
        code=ELE_7_REGEX_FAIL,
        level="ELE",
        description="Data element does not match required regex pattern",
        ak_code="7",
        ik_code="7",
    ),
    ELE_7_INVALID_CODE: ErrorCodeSpec(
        code=ELE_7_INVALID_CODE,
        level="ELE",
        description="Data element value not in valid code list",
        ak_code="7",
        ik_code="7",
    ),
    ELE_8_INVALID_DATE: ErrorCodeSpec(
        code=ELE_8_INVALID_DATE,
        level="ELE",
        description="Data element contains an invalid date (D8/D6/DT)",
        ak_code="8",
        ik_code="8",
    ),
    ELE_8_INVALID_DATE_RANGE: ErrorCodeSpec(
        code=ELE_8_INVALID_DATE_RANGE,
        level="ELE",
        description="Data element contains an invalid date range (RD8)",
        ak_code="8",
        ik_code="8",
    ),
    ELE_9_INVALID_TIME: ErrorCodeSpec(
        code=ELE_9_INVALID_TIME,
        level="ELE",
        description="Data element contains an invalid time (TM)",
        ak_code="9",
        ik_code="9",
    ),
    ELE_9_INVALID_TIME_OF_DAY: ErrorCodeSpec(
        code=ELE_9_INVALID_TIME_OF_DAY,
        level="ELE",
        description="Data element contains an invalid time-of-day value",
        ak_code="9",
        ik_code="9",
    ),
    ELE_10_NOT_USED: ErrorCodeSpec(
        code=ELE_10_NOT_USED,
        level="ELE",
        description="Data element marked Not Used (usage='N')",
        ak_code="10",
        ik_code="10",
    ),
    # --- Composite-level ---
    COMP_1_MANDATORY_MISSING: ErrorCodeSpec(
        code=COMP_1_MANDATORY_MISSING,
        level="ELE",  # composites surface as element-level errors in IK4/AK4
        description="Mandatory composite element missing",
        ak_code="1",
        ik_code="1",
    ),
    COMP_3_TOO_MANY_SUBELEMENTS: ErrorCodeSpec(
        code=COMP_3_TOO_MANY_SUBELEMENTS,
        level="ELE",
        description="Composite has too many sub-elements",
        ak_code="3",
        ik_code="3",
    ),
    COMP_5_NOT_USED: ErrorCodeSpec(
        code=COMP_5_NOT_USED,
        level="ELE",
        description="Composite marked Not Used (usage='N')",
        ak_code="5",
        ik_code="5",
    ),
    # --- Segment-level: validator ---
    SEG_3_TOO_MANY_ELEMENTS: ErrorCodeSpec(
        code=SEG_3_TOO_MANY_ELEMENTS,
        level="SEG",
        description="Segment has too many elements",
        ak_code="3",
        ik_code="3",
    ),
    SEG_3_TOO_MANY_SUBELEMENTS: ErrorCodeSpec(
        code=SEG_3_TOO_MANY_SUBELEMENTS,
        level="SEG",
        description="Segment has too many sub-elements in a composite",
        ak_code="3",
        ik_code="3",
    ),
    SEG_2_SYNTAX_RELATIONAL: ErrorCodeSpec(
        code=SEG_2_SYNTAX_RELATIONAL,
        level="SEG",
        description="Segment syntax rule (relational) violated",
        ak_code="2",
        ik_code="2",
    ),
    SEG_10_SYNTAX_EXCLUSIVE: ErrorCodeSpec(
        code=SEG_10_SYNTAX_EXCLUSIVE,
        level="SEG",
        description="Segment syntax rule (exclusive) violated",
        ak_code="10",
        ik_code="10",
    ),
    # --- Segment-level: walker ---
    SEG_1_SEGMENT_NOT_FOUND: ErrorCodeSpec(
        code=SEG_1_SEGMENT_NOT_FOUND,
        level="SEG",
        description="Unrecognized segment ID",
        ak_code="1",
        ik_code="1",
    ),
    SEG_2_SEGMENT_NOT_USED: ErrorCodeSpec(
        code=SEG_2_SEGMENT_NOT_USED,
        level="SEG",
        description="Segment marked Not Used (usage='N')",
        ak_code="2",
        ik_code="2",
    ),
    SEG_2_LOOP_NOT_USED: ErrorCodeSpec(
        code=SEG_2_LOOP_NOT_USED,
        level="SEG",
        description="Loop marked Not Used (usage='N')",
        ak_code="2",
        ik_code="2",
    ),
    SEG_3_MANDATORY_SEGMENT_MISSING: ErrorCodeSpec(
        code=SEG_3_MANDATORY_SEGMENT_MISSING,
        level="SEG",
        description="Mandatory segment missing",
        ak_code="3",
        ik_code="3",
    ),
    SEG_3_MANDATORY_LOOP_MISSING: ErrorCodeSpec(
        code=SEG_3_MANDATORY_LOOP_MISSING,
        level="SEG",
        description="Mandatory loop missing",
        ak_code="3",
        ik_code="3",
    ),
    SEG_5_SEGMENT_REPEAT_EXCEEDED: ErrorCodeSpec(
        code=SEG_5_SEGMENT_REPEAT_EXCEEDED,
        level="SEG",
        description="Segment repeat count exceeded (segment exceeds maximum use)",
        ak_code="5",
        ik_code="5",
    ),
    SEG_4_LOOP_REPEAT_EXCEEDED: ErrorCodeSpec(
        code=SEG_4_LOOP_REPEAT_EXCEEDED,
        level="SEG",
        description="Loop repeat count exceeded (loop occurs over maximum times)",
        ak_code="4",
        ik_code="4",
    ),
    # --- Segment-level: parser ---
    SEG_1_INVALID_SEG_ID: ErrorCodeSpec(
        code=SEG_1_INVALID_SEG_ID,
        level="SEG",
        description="Segment identifier is malformed (parser-time invalid seg ID)",
        ak_code="1",
        ik_code="1",
    ),
    SEG_1_LEADING_SPACE: ErrorCodeSpec(
        code=SEG_1_LEADING_SPACE,
        level="SEG",
        description="Segment line started with leading whitespace (parser-time)",
        ak_code="1",
        ik_code="1",
    ),
    SEG_8_HAS_DATA_ELEMENT_ERRORS: ErrorCodeSpec(
        code=SEG_8_HAS_DATA_ELEMENT_ERRORS,
        level="SEG",
        description=(
            "Segment has data element errors. Used by apply_segment_errors "
            "to roll up element-level validator errors (too-many-elements, "
            "syntax violations, mandatory composite missing, etc.) into a "
            "spec-correct IK3-04 / AK3-04 code per PR #161. The original "
            "element-level pyx12 code is preserved in the err_str."
        ),
        ak_code="8",
        ik_code="8",
    ),
    SEG_8_SEGMENT_EMPTY: ErrorCodeSpec(
        code=SEG_8_SEGMENT_EMPTY,
        level="SEG",
        description="Segment is empty (parser-time)",
        ak_code="8",
        ik_code="8",
    ),
    # SEG_8_TRAILING_TERMINATORS captures the historical "SEG1" code which
    # the visitors inline-remapped to AK/IK "8". This table entry replaces
    # the inline remap.
    SEG_8_TRAILING_TERMINATORS: ErrorCodeSpec(
        code=SEG_8_TRAILING_TERMINATORS,
        level="SEG",
        description="Segment has trailing element terminators (was 'SEG1')",
        ak_code="8",
        ik_code="8",
    ),
    # HL1/HL2/LX historically had no ack remap (filtered out by the visitor's
    # valid_*_codes tuples). Preserve that behavior with ak_code=ik_code=None
    # so producer migration in PR 4 doesn't accidentally surface them.
    SEG_8_HL_COUNT_MISMATCH: ErrorCodeSpec(
        code=SEG_8_HL_COUNT_MISMATCH,
        level="SEG",
        description="HL count does not match self-reported HL01 (was 'HL1')",
        ak_code=None,
        ik_code=None,
    ),
    SEG_8_HL_INVALID_PARENT: ErrorCodeSpec(
        code=SEG_8_HL_INVALID_PARENT,
        level="SEG",
        description="HL parent reference is not on the HL stack (was 'HL2')",
        ak_code=None,
        ik_code=None,
    ),
    SEG_8_LX_COUNT_MISMATCH: ErrorCodeSpec(
        code=SEG_8_LX_COUNT_MISMATCH,
        level="SEG",
        description="2400/LX01 service line number does not match running count (was 'LX')",
        ak_code=None,
        ik_code=None,
    ),
}


def x12_code_for(err_cde: str, prefer_5010: bool = True) -> str | None:
    """Resolve a pyx12 error code to its X12 ack code.

    Returns None for codes that do not surface in the requested ack
    channel (e.g. the SEG_8_HL_* parser codes that historically were
    filtered out).

    Falls through to err_cde unchanged when err_cde is not a pyx12
    code (legacy X12 codes like "6" / "8" emitted by un-migrated
    producers during the PR 1-4 transition). PR 5 removes that
    fallthrough — once all producers emit pyx12 codes only, an unknown
    err_cde is an error.
    """
    spec = ERROR_CODES.get(err_cde)
    if spec is None:
        # Legacy raw X12 code; pass through unchanged.
        return err_cde
    if prefer_5010:
        return spec.ik_code if spec.ik_code is not None else spec.ak_code
    return spec.ak_code if spec.ak_code is not None else spec.ik_code
