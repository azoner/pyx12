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

    x12_description is the official X12 spec definition for the error code
    (e.g., "Required Data Element Missing" for IK4-03 code "1"). Provides
    cross-reference to the X12 Implementation Guide.
    """

    code: str
    level: LevelT
    description: str
    ak_code: str | None
    ik_code: str | None
    x12_description: str


# Element-level pyx12 codes. Module-level constants pair with each
# ERROR_CODES entry for IDE auto-complete and CLI grep-ability.
# Sorted: numeric X12 codes (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13),
# then implementation-dependent codes (I6, I9, I10, I11, I12, I13).
ELE_1_MANDATORY_MISSING = "ELE_1_mandatory_missing"
ELE_2_CONDITIONAL_MISSING = "ELE_2_conditional_missing"
ELE_3_TOO_MANY_ELEMENTS = "ELE_3_too_many_elements"
ELE_4_TOO_SHORT = "ELE_4_too_short"
ELE_5_TOO_LONG = "ELE_5_too_long"
ELE_6_INVALID_COMPOSITE = "ELE_6_invalid_composite"
ELE_6_TRAILING_SPACE = "ELE_6_trailing_space"
ELE_6_CONTROL_CHAR = "ELE_6_control_char"
ELE_6_INVALID_TYPE_CHAR = "ELE_6_invalid_type_char"
ELE_7_INVALID_CODE = "ELE_7_invalid_code"
ELE_7_REGEX_FAIL = "ELE_7_regex_fail"
ELE_8_INVALID_DATE = "ELE_8_invalid_date"
ELE_8_INVALID_DATE_RANGE = "ELE_8_invalid_date_range"
ELE_9_INVALID_TIME = "ELE_9_invalid_time"
ELE_9_INVALID_TIME_OF_DAY = "ELE_9_invalid_time_of_day"
ELE_10_SYNTAX_EXCLUSIVE = "ELE_10_syntax_exclusive"
ELE_12_TOO_MANY_REPETITIONS = "ELE_12_too_many_repetitions"
ELE_13_TOO_MANY_COMPONENTS = "ELE_13_too_many_components"
ELE_I10_NOT_USED = "ELE_I10_NOT_USED"
ELE_I11_TOO_FEW_REPETITIONS = "ELE_I11_too_few_repetitions"
ELE_I13_SITUATIONAL_NOT_USED = "ELE_I13_situational_not_used"

# Composite-level pyx12 codes. Composites historically emitted via
# EleError carrying the seg_error code semantics (see _composite.py).
# Sorted: numeric X12 codes (1, 3, 5).
COMP_1_MANDATORY_MISSING = "COMP_1_mandatory_missing"
COMP_3_TOO_MANY_SUBELEMENTS = "COMP_3_too_many_subelements"
COMP_5_NOT_USED = "COMP_5_not_used"

# Segment-level pyx12 codes.
# Sorted: numeric X12 codes (1, 2, 3, 4, 5, 8, 10), then non-numeric.
# Codes 1-5 are validator / walker / parser sources; code 8 is
# synthetic (apply_segment_errors rollup + parser HL/LX series).
SEG_1_SEGMENT_NOT_FOUND = "SEG_1_segment_not_found"
SEG_1_INVALID_SEG_ID = "SEG_1_invalid_seg_id"
SEG_1_LEADING_SPACE = "SEG_1_leading_space"
SEG_2_SYNTAX_RELATIONAL = "SEG_2_syntax_relational"
SEG_2_SEGMENT_NOT_USED = "SEG_2_segment_not_used"
SEG_2_LOOP_NOT_USED = "SEG_2_loop_not_used"
SEG_3_TOO_MANY_ELEMENTS = "SEG_3_too_many_elements"
SEG_3_TOO_MANY_SUBELEMENTS = "SEG_3_too_many_subelements"
SEG_3_MANDATORY_SEGMENT_MISSING = "SEG_3_mandatory_segment_missing"
SEG_3_MANDATORY_LOOP_MISSING = "SEG_3_mandatory_loop_missing"
SEG_4_LOOP_REPEAT_EXCEEDED = "SEG_4_loop_repeat_exceeded"
SEG_5_SEGMENT_REPEAT_EXCEEDED = "SEG_5_segment_repeat_exceeded"
SEG_8_HAS_DATA_ELEMENT_ERRORS = "SEG_8_has_data_element_errors"
SEG_8_SEGMENT_EMPTY = "SEG_8_segment_empty"
SEG_8_TRAILING_TERMINATORS = "SEG_8_trailing_terminators"
SEG_8_HL_COUNT_MISMATCH = "SEG_8_hl_count_mismatch"
SEG_8_HL_INVALID_PARENT = "SEG_8_hl_invalid_parent"
SEG_8_LX_COUNT_MISMATCH = "SEG_8_lx_count_mismatch"
SEG_10_SYNTAX_EXCLUSIVE = "SEG_10_syntax_exclusive"

# Interchange (ISA) level pyx12 codes. Surface as TA1 Interchange Note
# Codes (TA105) per X12 spec. Sorted: numeric codes 000–031.
ISA_000_NO_ERROR = "ISA_000_no_error"
ISA_001_CONTROL_NUMBER_MISMATCH = "ISA_001_control_number_mismatch"
ISA_002_STANDARDS_NOT_SUPPORTED = "ISA_002_standards_not_supported"
ISA_003_VERSION_NOT_SUPPORTED = "ISA_003_version_not_supported"
ISA_004_INVALID_SEGMENT_TERMINATOR = "ISA_004_invalid_segment_terminator"
ISA_005_INVALID_SENDER_QUALIFIER = "ISA_005_invalid_sender_qualifier"
ISA_006_INVALID_SENDER_ID = "ISA_006_invalid_sender_id"
ISA_007_INVALID_RECEIVER_QUALIFIER = "ISA_007_invalid_receiver_qualifier"
ISA_008_INVALID_RECEIVER_ID = "ISA_008_invalid_receiver_id"
ISA_009_UNKNOWN_RECEIVER_ID = "ISA_009_unknown_receiver_id"
ISA_010_INVALID_AUTH_QUALIFIER = "ISA_010_invalid_auth_qualifier"
ISA_011_INVALID_AUTH_INFO = "ISA_011_invalid_auth_info"
ISA_012_INVALID_SECURITY_QUALIFIER = "ISA_012_invalid_security_qualifier"
ISA_013_INVALID_SECURITY_INFO = "ISA_013_invalid_security_info"
ISA_014_INVALID_DATE = "ISA_014_invalid_date"
ISA_015_INVALID_TIME = "ISA_015_invalid_time"
ISA_016_INVALID_STANDARDS_ID = "ISA_016_invalid_standards_id"
ISA_017_INVALID_VERSION_ID = "ISA_017_invalid_version_id"
ISA_018_INVALID_CONTROL_NUMBER = "ISA_018_invalid_control_number"
ISA_019_INVALID_ACK_REQUESTED = "ISA_019_invalid_ack_requested"
ISA_020_INVALID_TEST_INDICATOR = "ISA_020_invalid_test_indicator"
ISA_021_INVALID_GROUP_COUNT = "ISA_021_invalid_group_count"
ISA_022_INVALID_CONTROL_STRUCTURE = "ISA_022_invalid_control_structure"
ISA_023_PREMATURE_EOF = "ISA_023_premature_eof"
ISA_024_INVALID_CONTENT = "ISA_024_invalid_content"
ISA_025_DUPLICATE_CONTROL_NUMBER = "ISA_025_duplicate_control_number"
ISA_026_INVALID_DATA_ELEMENT_SEPARATOR = "ISA_026_invalid_data_element_separator"
ISA_027_INVALID_COMPONENT_SEPARATOR = "ISA_027_invalid_component_separator"
ISA_028_INVALID_DELIVERY_DATE = "ISA_028_invalid_delivery_date"
ISA_029_INVALID_DELIVERY_TIME = "ISA_029_invalid_delivery_time"
ISA_030_INVALID_DELIVERY_TIME_CODE = "ISA_030_invalid_delivery_time_code"
ISA_031_INVALID_GRADE_OF_SERVICE = "ISA_031_invalid_grade_of_service"


ERROR_CODES: dict[str, ErrorCodeSpec] = {
    # --- Element-level: sorted by numeric X12 code (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13) ---
    ELE_1_MANDATORY_MISSING: ErrorCodeSpec(
        code=ELE_1_MANDATORY_MISSING,
        level="ELE",
        description="Mandatory data element missing",
        ak_code="1",
        ik_code="1",
        x12_description="Required Data Element Missing",
    ),
    ELE_2_CONDITIONAL_MISSING: ErrorCodeSpec(
        code=ELE_2_CONDITIONAL_MISSING,
        level="ELE",
        description="Conditional required data element missing",
        ak_code="2",
        ik_code="2",
        x12_description="Conditional Required Data Element Missing",
    ),
    ELE_3_TOO_MANY_ELEMENTS: ErrorCodeSpec(
        code=ELE_3_TOO_MANY_ELEMENTS,
        level="ELE",
        description="Too many data elements",
        ak_code="3",
        ik_code="3",
        x12_description="Too Many Data Elements",
    ),
    ELE_4_TOO_SHORT: ErrorCodeSpec(
        code=ELE_4_TOO_SHORT,
        level="ELE",
        description="Data element too short",
        ak_code="4",
        ik_code="4",
        x12_description="Data Element Too Short",
    ),
    ELE_5_TOO_LONG: ErrorCodeSpec(
        code=ELE_5_TOO_LONG,
        level="ELE",
        description="Data element too long",
        ak_code="5",
        ik_code="5",
        x12_description="Data Element Too Long",
    ),
    ELE_6_INVALID_COMPOSITE: ErrorCodeSpec(
        code=ELE_6_INVALID_COMPOSITE,
        level="ELE",
        description="Composite element used at non-composite position",
        ak_code="6",
        ik_code="6",
        x12_description="Invalid Character In Data Element",
    ),
    ELE_6_TRAILING_SPACE: ErrorCodeSpec(
        code=ELE_6_TRAILING_SPACE,
        level="ELE",
        description="Trailing space in data element",
        ak_code="6",
        ik_code="6",
        x12_description="Invalid Character In Data Element",
    ),
    ELE_6_CONTROL_CHAR: ErrorCodeSpec(
        code=ELE_6_CONTROL_CHAR,
        level="ELE",
        description="Control character in data element",
        ak_code="6",
        ik_code="6",
        x12_description="Invalid Character In Data Element",
    ),
    ELE_6_INVALID_TYPE_CHAR: ErrorCodeSpec(
        code=ELE_6_INVALID_TYPE_CHAR,
        level="ELE",
        description="Invalid character for declared element data type",
        ak_code="6",
        ik_code="6",
        x12_description="Invalid Character In Data Element",
    ),
    ELE_7_INVALID_CODE: ErrorCodeSpec(
        code=ELE_7_INVALID_CODE,
        level="ELE",
        description="Data element value not in valid code list",
        ak_code="7",
        ik_code="7",
        x12_description="Invalid Code Value",
    ),
    ELE_7_REGEX_FAIL: ErrorCodeSpec(
        code=ELE_7_REGEX_FAIL,
        level="ELE",
        description="Data element does not match required regex pattern",
        ak_code="7",
        ik_code="7",
        x12_description="Invalid Code Value",
    ),
    ELE_8_INVALID_DATE: ErrorCodeSpec(
        code=ELE_8_INVALID_DATE,
        level="ELE",
        description="Data element contains an invalid date (D8/D6/DT)",
        ak_code="8",
        ik_code="8",
        x12_description="Invalid Date",
    ),
    ELE_8_INVALID_DATE_RANGE: ErrorCodeSpec(
        code=ELE_8_INVALID_DATE_RANGE,
        level="ELE",
        description="Data element contains an invalid date range (RD8)",
        ak_code="8",
        ik_code="8",
        x12_description="Invalid Date",
    ),
    ELE_9_INVALID_TIME: ErrorCodeSpec(
        code=ELE_9_INVALID_TIME,
        level="ELE",
        description="Data element contains an invalid time (TM)",
        ak_code="9",
        ik_code="9",
        x12_description="Invalid Time",
    ),
    ELE_9_INVALID_TIME_OF_DAY: ErrorCodeSpec(
        code=ELE_9_INVALID_TIME_OF_DAY,
        level="ELE",
        description="Data element contains an invalid time-of-day value",
        ak_code="9",
        ik_code="9",
        x12_description="Invalid Time",
    ),
    ELE_10_SYNTAX_EXCLUSIVE: ErrorCodeSpec(
        code=ELE_10_SYNTAX_EXCLUSIVE,
        level="ELE",
        description="Exclusion Condition Violated",
        ak_code="10",
        ik_code="10",
        x12_description="Exclusion Condition Violated",
    ),
    ELE_12_TOO_MANY_REPETITIONS: ErrorCodeSpec(
        code=ELE_12_TOO_MANY_REPETITIONS,
        level="ELE",
        description="Too many repetitions of data element",
        ak_code="12",
        ik_code="12",
        x12_description="Too Many Repetitions",
    ),
    ELE_13_TOO_MANY_COMPONENTS: ErrorCodeSpec(
        code=ELE_13_TOO_MANY_COMPONENTS,
        level="ELE",
        description="Too many components in data element",
        ak_code="13",
        ik_code="13",
        x12_description="Too Many Components",
    ),
    ELE_I10_NOT_USED: ErrorCodeSpec(
        code=ELE_I10_NOT_USED,
        level="ELE",
        description="Implementation: data element marked Not Used (usage='N')",
        ak_code=None,
        ik_code="I10",
        x12_description="Implementation 'Not Used' Data Element Present",
    ),
    ELE_I11_TOO_FEW_REPETITIONS: ErrorCodeSpec(
        code=ELE_I11_TOO_FEW_REPETITIONS,
        level="ELE",
        description="Too few repetitions of data element",
        ak_code=None,
        ik_code="I11",
        x12_description="Too Few Repetitions",
    ),
    ELE_I13_SITUATIONAL_NOT_USED: ErrorCodeSpec(
        code=ELE_I13_SITUATIONAL_NOT_USED,
        level="ELE",
        description="Implementation: data element marked situational Not Used",
        ak_code=None,
        ik_code="I13",
        x12_description="Implementation Dependent 'Not Used' Data Element Present",
    ),
    # --- Composite-level: sorted by numeric X12 code (1, 3, 5) ---
    COMP_1_MANDATORY_MISSING: ErrorCodeSpec(
        code=COMP_1_MANDATORY_MISSING,
        level="ELE",
        description="Mandatory composite element missing",
        ak_code="1",
        ik_code="1",
        x12_description="Required Data Element Missing",
    ),
    COMP_3_TOO_MANY_SUBELEMENTS: ErrorCodeSpec(
        code=COMP_3_TOO_MANY_SUBELEMENTS,
        level="ELE",
        description="Composite has too many sub-elements",
        ak_code="3",
        ik_code="3",
        x12_description="Too Many Data Elements",
    ),
    COMP_5_NOT_USED: ErrorCodeSpec(
        code=COMP_5_NOT_USED,
        level="ELE",
        description="Composite marked Not Used (usage='N')",
        ak_code="5",
        ik_code="I10",
        x12_description="Implementation 'Not Used' Data Element Present (5010)",
    ),
    # --- Segment-level: sorted by numeric X12 code (1, 2, 3, 4, 5, 8, 10),
    # then non-numeric for code 8 (multiple sub-codes) ---
    SEG_1_SEGMENT_NOT_FOUND: ErrorCodeSpec(
        code=SEG_1_SEGMENT_NOT_FOUND,
        level="SEG",
        description="Unrecognized segment ID",
        ak_code="1",
        ik_code="1",
        x12_description="Unrecognized segment ID",
    ),
    SEG_1_INVALID_SEG_ID: ErrorCodeSpec(
        code=SEG_1_INVALID_SEG_ID,
        level="SEG",
        description="Segment identifier is malformed (parser-time invalid seg ID)",
        ak_code="1",
        ik_code="1",
        x12_description="Unrecognized segment ID",
    ),
    SEG_1_LEADING_SPACE: ErrorCodeSpec(
        code=SEG_1_LEADING_SPACE,
        level="SEG",
        description="Segment line started with leading whitespace (parser-time)",
        ak_code="1",
        ik_code="1",
        x12_description="Unrecognized segment ID",
    ),
    SEG_2_SYNTAX_RELATIONAL: ErrorCodeSpec(
        code=SEG_2_SYNTAX_RELATIONAL,
        level="SEG",
        description="Segment syntax rule (relational) violated",
        ak_code="2",
        ik_code="2",
        x12_description="Unexpected segment",
    ),
    SEG_2_SEGMENT_NOT_USED: ErrorCodeSpec(
        code=SEG_2_SEGMENT_NOT_USED,
        level="SEG",
        description="Segment marked Not Used (usage='N')",
        ak_code="2",
        ik_code="I4",
        x12_description="Implementation 'Not Used' Segment Present",
    ),
    SEG_2_LOOP_NOT_USED: ErrorCodeSpec(
        code=SEG_2_LOOP_NOT_USED,
        level="SEG",
        description="Loop marked Not Used (usage='N')",
        ak_code="2",
        ik_code="I4",
        x12_description="Implementation 'Not Used' Segment Present",
    ),
    SEG_3_TOO_MANY_ELEMENTS: ErrorCodeSpec(
        code=SEG_3_TOO_MANY_ELEMENTS,
        level="SEG",
        description="Segment has too many elements",
        ak_code="3",
        ik_code="3",
        x12_description="Required Segment Missing",
    ),
    SEG_3_TOO_MANY_SUBELEMENTS: ErrorCodeSpec(
        code=SEG_3_TOO_MANY_SUBELEMENTS,
        level="SEG",
        description="Segment has too many sub-elements in a composite",
        ak_code="3",
        ik_code="3",
        x12_description="Required Segment Missing",
    ),
    SEG_3_MANDATORY_SEGMENT_MISSING: ErrorCodeSpec(
        code=SEG_3_MANDATORY_SEGMENT_MISSING,
        level="SEG",
        description="Mandatory segment missing",
        ak_code="3",
        ik_code="3",
        x12_description="Required Segment Missing",
    ),
    SEG_3_MANDATORY_LOOP_MISSING: ErrorCodeSpec(
        code=SEG_3_MANDATORY_LOOP_MISSING,
        level="SEG",
        description="Mandatory loop missing",
        ak_code="3",
        ik_code="3",
        x12_description="Required Segment Missing",
    ),
    SEG_4_LOOP_REPEAT_EXCEEDED: ErrorCodeSpec(
        code=SEG_4_LOOP_REPEAT_EXCEEDED,
        level="SEG",
        description="Loop repeat count exceeded (loop occurs over maximum times)",
        ak_code="4",
        ik_code="4",
        x12_description="Loop Occurs Over Maximum Times",
    ),
    SEG_5_SEGMENT_REPEAT_EXCEEDED: ErrorCodeSpec(
        code=SEG_5_SEGMENT_REPEAT_EXCEEDED,
        level="SEG",
        description="Segment repeat count exceeded (segment exceeds maximum use)",
        ak_code="5",
        ik_code="5",
        x12_description="Segment Exceeds Maximum Use",
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
        x12_description="Segment Has Data Element Errors",
    ),
    SEG_8_SEGMENT_EMPTY: ErrorCodeSpec(
        code=SEG_8_SEGMENT_EMPTY,
        level="SEG",
        description="Segment is empty (parser-time)",
        ak_code="8",
        ik_code="8",
        x12_description="Segment Has Data Element Errors",
    ),
    SEG_8_TRAILING_TERMINATORS: ErrorCodeSpec(
        code=SEG_8_TRAILING_TERMINATORS,
        level="SEG",
        description="Segment has trailing element terminators (was 'SEG1')",
        ak_code="8",
        ik_code="8",
        x12_description="Segment Has Data Element Errors",
    ),
    SEG_8_HL_COUNT_MISMATCH: ErrorCodeSpec(
        code=SEG_8_HL_COUNT_MISMATCH,
        level="SEG",
        description="HL count does not match self-reported HL01 (was 'HL1')",
        ak_code=None,
        ik_code=None,
        x12_description="Segment Has Data Element Errors",
    ),
    SEG_8_HL_INVALID_PARENT: ErrorCodeSpec(
        code=SEG_8_HL_INVALID_PARENT,
        level="SEG",
        description="HL parent reference is not on the HL stack (was 'HL2')",
        ak_code=None,
        ik_code=None,
        x12_description="Segment Has Data Element Errors",
    ),
    SEG_8_LX_COUNT_MISMATCH: ErrorCodeSpec(
        code=SEG_8_LX_COUNT_MISMATCH,
        level="SEG",
        description="2400/LX01 service line number does not match running count (was 'LX')",
        ak_code=None,
        ik_code=None,
        x12_description="Segment Has Data Element Errors",
    ),
    SEG_10_SYNTAX_EXCLUSIVE: ErrorCodeSpec(
        code=SEG_10_SYNTAX_EXCLUSIVE,
        level="SEG",
        description="Segment syntax rule (exclusive) violated",
        ak_code="10",
        ik_code="10",
        x12_description="Exclusion Condition Violated",
    ),
    # --- Interchange-level: TA1 Interchange Note Codes (TA105), 000–031.
    # ak_code == ik_code for all entries since TA1 is shared between
    # 4010 and 5010 (same I18 element).
    ISA_000_NO_ERROR: ErrorCodeSpec(
        code=ISA_000_NO_ERROR,
        level="ISA",
        description="No interchange error",
        ak_code="000",
        ik_code="000",
        x12_description="No Error",
    ),
    ISA_001_CONTROL_NUMBER_MISMATCH: ErrorCodeSpec(
        code=ISA_001_CONTROL_NUMBER_MISMATCH,
        level="ISA",
        description="ISA13 and IEA02 control numbers do not match",
        ak_code="001",
        ik_code="001",
        x12_description="The Interchange Control Number in the Header and Trailer Do Not Match",
    ),
    ISA_002_STANDARDS_NOT_SUPPORTED: ErrorCodeSpec(
        code=ISA_002_STANDARDS_NOT_SUPPORTED,
        level="ISA",
        description="ISA11 control standards identifier is not supported",
        ak_code="002",
        ik_code="002",
        x12_description="Standards in ISA11 (Control Standards) is not supported",
    ),
    ISA_003_VERSION_NOT_SUPPORTED: ErrorCodeSpec(
        code=ISA_003_VERSION_NOT_SUPPORTED,
        level="ISA",
        description="Version of controls is not supported",
        ak_code="003",
        ik_code="003",
        x12_description="Version of controls is not supported",
    ),
    ISA_004_INVALID_SEGMENT_TERMINATOR: ErrorCodeSpec(
        code=ISA_004_INVALID_SEGMENT_TERMINATOR,
        level="ISA",
        description="Segment terminator is invalid",
        ak_code="004",
        ik_code="004",
        x12_description="Segment Terminator is Invalid",
    ),
    ISA_005_INVALID_SENDER_QUALIFIER: ErrorCodeSpec(
        code=ISA_005_INVALID_SENDER_QUALIFIER,
        level="ISA",
        description="ISA05 invalid interchange ID qualifier for sender",
        ak_code="005",
        ik_code="005",
        x12_description="Invalid Interchange ID Qualifier for Sender",
    ),
    ISA_006_INVALID_SENDER_ID: ErrorCodeSpec(
        code=ISA_006_INVALID_SENDER_ID,
        level="ISA",
        description="ISA06 invalid interchange sender ID",
        ak_code="006",
        ik_code="006",
        x12_description="Invalid Interchange Sender ID",
    ),
    ISA_007_INVALID_RECEIVER_QUALIFIER: ErrorCodeSpec(
        code=ISA_007_INVALID_RECEIVER_QUALIFIER,
        level="ISA",
        description="ISA07 invalid interchange ID qualifier for receiver",
        ak_code="007",
        ik_code="007",
        x12_description="Invalid Interchange ID Qualifier for Receiver",
    ),
    ISA_008_INVALID_RECEIVER_ID: ErrorCodeSpec(
        code=ISA_008_INVALID_RECEIVER_ID,
        level="ISA",
        description="ISA08 invalid interchange receiver ID",
        ak_code="008",
        ik_code="008",
        x12_description="Invalid Interchange Receiver ID",
    ),
    ISA_009_UNKNOWN_RECEIVER_ID: ErrorCodeSpec(
        code=ISA_009_UNKNOWN_RECEIVER_ID,
        level="ISA",
        description="ISA08 receiver ID is not known to this trading partner",
        ak_code="009",
        ik_code="009",
        x12_description="Unknown Interchange Receiver ID",
    ),
    ISA_010_INVALID_AUTH_QUALIFIER: ErrorCodeSpec(
        code=ISA_010_INVALID_AUTH_QUALIFIER,
        level="ISA",
        description="ISA01 invalid authorization information qualifier",
        ak_code="010",
        ik_code="010",
        x12_description="Invalid Authorization Information Qualifier",
    ),
    ISA_011_INVALID_AUTH_INFO: ErrorCodeSpec(
        code=ISA_011_INVALID_AUTH_INFO,
        level="ISA",
        description="ISA02 invalid authorization information",
        ak_code="011",
        ik_code="011",
        x12_description="Invalid Authorization Information",
    ),
    ISA_012_INVALID_SECURITY_QUALIFIER: ErrorCodeSpec(
        code=ISA_012_INVALID_SECURITY_QUALIFIER,
        level="ISA",
        description="ISA03 invalid security information qualifier",
        ak_code="012",
        ik_code="012",
        x12_description="Invalid Security Information Qualifier",
    ),
    ISA_013_INVALID_SECURITY_INFO: ErrorCodeSpec(
        code=ISA_013_INVALID_SECURITY_INFO,
        level="ISA",
        description="ISA04 invalid security information",
        ak_code="013",
        ik_code="013",
        x12_description="Invalid Security Information",
    ),
    ISA_014_INVALID_DATE: ErrorCodeSpec(
        code=ISA_014_INVALID_DATE,
        level="ISA",
        description="ISA09 invalid interchange date",
        ak_code="014",
        ik_code="014",
        x12_description="Invalid Interchange Date",
    ),
    ISA_015_INVALID_TIME: ErrorCodeSpec(
        code=ISA_015_INVALID_TIME,
        level="ISA",
        description="ISA10 invalid interchange time",
        ak_code="015",
        ik_code="015",
        x12_description="Invalid Interchange Time",
    ),
    ISA_016_INVALID_STANDARDS_ID: ErrorCodeSpec(
        code=ISA_016_INVALID_STANDARDS_ID,
        level="ISA",
        description="ISA11 invalid interchange standards identifier",
        ak_code="016",
        ik_code="016",
        x12_description="Invalid Interchange Standards Identifier",
    ),
    ISA_017_INVALID_VERSION_ID: ErrorCodeSpec(
        code=ISA_017_INVALID_VERSION_ID,
        level="ISA",
        description="ISA12 invalid interchange version ID",
        ak_code="017",
        ik_code="017",
        x12_description="Invalid Interchange Version ID",
    ),
    ISA_018_INVALID_CONTROL_NUMBER: ErrorCodeSpec(
        code=ISA_018_INVALID_CONTROL_NUMBER,
        level="ISA",
        description="ISA13 invalid interchange control number",
        ak_code="018",
        ik_code="018",
        x12_description="Invalid Interchange Control Number",
    ),
    ISA_019_INVALID_ACK_REQUESTED: ErrorCodeSpec(
        code=ISA_019_INVALID_ACK_REQUESTED,
        level="ISA",
        description="ISA14 invalid acknowledgment requested value",
        ak_code="019",
        ik_code="019",
        x12_description="Invalid Acknowledgment Requested",
    ),
    ISA_020_INVALID_TEST_INDICATOR: ErrorCodeSpec(
        code=ISA_020_INVALID_TEST_INDICATOR,
        level="ISA",
        description="ISA15 invalid usage/test indicator",
        ak_code="020",
        ik_code="020",
        x12_description="Invalid Test Indicator",
    ),
    ISA_021_INVALID_GROUP_COUNT: ErrorCodeSpec(
        code=ISA_021_INVALID_GROUP_COUNT,
        level="ISA",
        description="IEA01 included-group count does not match received GS count",
        ak_code="021",
        ik_code="021",
        x12_description="Invalid Number of Included Groups",
    ),
    ISA_022_INVALID_CONTROL_STRUCTURE: ErrorCodeSpec(
        code=ISA_022_INVALID_CONTROL_STRUCTURE,
        level="ISA",
        description="Interchange control structure is invalid (e.g. ISA loop missing both TA1 and GS_LOOP)",
        ak_code="022",
        ik_code="022",
        x12_description="Invalid Control Structure",
    ),
    ISA_023_PREMATURE_EOF: ErrorCodeSpec(
        code=ISA_023_PREMATURE_EOF,
        level="ISA",
        description="Improper (premature) end-of-file before IEA",
        ak_code="023",
        ik_code="023",
        x12_description="Improper (Premature) End-of-File",
    ),
    ISA_024_INVALID_CONTENT: ErrorCodeSpec(
        code=ISA_024_INVALID_CONTENT,
        level="ISA",
        description="Invalid interchange content (e.g. invalid GS segment, unterminated GS loop)",
        ak_code="024",
        ik_code="024",
        x12_description="Invalid Interchange Content (e.g., Invalid GS segment)",
    ),
    ISA_025_DUPLICATE_CONTROL_NUMBER: ErrorCodeSpec(
        code=ISA_025_DUPLICATE_CONTROL_NUMBER,
        level="ISA",
        description="ISA13 interchange control number not unique within file",
        ak_code="025",
        ik_code="025",
        x12_description="Duplicate Interchange Control Number",
    ),
    ISA_026_INVALID_DATA_ELEMENT_SEPARATOR: ErrorCodeSpec(
        code=ISA_026_INVALID_DATA_ELEMENT_SEPARATOR,
        level="ISA",
        description="Invalid data element separator",
        ak_code="026",
        ik_code="026",
        x12_description="Invalid Data Element Separator",
    ),
    ISA_027_INVALID_COMPONENT_SEPARATOR: ErrorCodeSpec(
        code=ISA_027_INVALID_COMPONENT_SEPARATOR,
        level="ISA",
        description="ISA16 invalid component element separator",
        ak_code="027",
        ik_code="027",
        x12_description="Invalid Component Element Separator",
    ),
    ISA_028_INVALID_DELIVERY_DATE: ErrorCodeSpec(
        code=ISA_028_INVALID_DELIVERY_DATE,
        level="ISA",
        description="Invalid delivery date in deferred delivery request",
        ak_code="028",
        ik_code="028",
        x12_description="Invalid Delivery Date in Deferred Delivery Request",
    ),
    ISA_029_INVALID_DELIVERY_TIME: ErrorCodeSpec(
        code=ISA_029_INVALID_DELIVERY_TIME,
        level="ISA",
        description="Invalid delivery time in deferred delivery request",
        ak_code="029",
        ik_code="029",
        x12_description="Invalid Delivery Time in Deferred Delivery Request",
    ),
    ISA_030_INVALID_DELIVERY_TIME_CODE: ErrorCodeSpec(
        code=ISA_030_INVALID_DELIVERY_TIME_CODE,
        level="ISA",
        description="Invalid delivery time code in deferred delivery request",
        ak_code="030",
        ik_code="030",
        x12_description="Invalid Delivery Time Code in Deferred Delivery Request",
    ),
    ISA_031_INVALID_GRADE_OF_SERVICE: ErrorCodeSpec(
        code=ISA_031_INVALID_GRADE_OF_SERVICE,
        level="ISA",
        description="Invalid grade of service",
        ak_code="031",
        ik_code="031",
        x12_description="Invalid Grade of Service",
    ),
}


# Element-position to ISA_* code maps for envelope segments. When an
# element validator raises a generic ELE_* error against an ISA or IEA
# element, apply_segment_errors upgrades the err_cde to the canonical
# TA1-level pyx12 code via these maps. Keeps element validators in
# map_if/ ignorant of envelope context.
ISA_ELE_POSITION_TO_CODE: dict[int, str] = {
    1: ISA_010_INVALID_AUTH_QUALIFIER,
    2: ISA_011_INVALID_AUTH_INFO,
    3: ISA_012_INVALID_SECURITY_QUALIFIER,
    4: ISA_013_INVALID_SECURITY_INFO,
    5: ISA_005_INVALID_SENDER_QUALIFIER,
    6: ISA_006_INVALID_SENDER_ID,
    7: ISA_007_INVALID_RECEIVER_QUALIFIER,
    8: ISA_008_INVALID_RECEIVER_ID,
    9: ISA_014_INVALID_DATE,
    10: ISA_015_INVALID_TIME,
    11: ISA_016_INVALID_STANDARDS_ID,
    12: ISA_017_INVALID_VERSION_ID,
    13: ISA_018_INVALID_CONTROL_NUMBER,
    14: ISA_019_INVALID_ACK_REQUESTED,
    15: ISA_020_INVALID_TEST_INDICATOR,
    16: ISA_027_INVALID_COMPONENT_SEPARATOR,
}

IEA_ELE_POSITION_TO_CODE: dict[int, str] = {
    1: ISA_021_INVALID_GROUP_COUNT,
    2: ISA_018_INVALID_CONTROL_NUMBER,
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
