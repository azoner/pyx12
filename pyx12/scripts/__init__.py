"""Helpers shared across the pyx12 CLI scripts."""

from __future__ import annotations

from pyx12.codes import list_external_codesets


def external_codes_help_epilog() -> str:
    """Build a `--help` epilog table listing names accepted by ``-x``.

    Sourced from ``codes.xml`` so the table never drifts. Used by scripts
    that expose ``--exclude-external-codes`` (x12valid, x12html, x12xml).
    """
    pairs = list_external_codesets()
    width = max((len(cid) for cid, _ in pairs), default=0)
    rows = "\n".join(f"  {cid:<{width}}  {name}" for cid, name in pairs)
    return (
        "External code names accepted by --exclude-external-codes / -x\n"
        "(pass the flag once per name to suppress validation against that "
        "codeset):\n\n"
        f"{rows}"
    )
