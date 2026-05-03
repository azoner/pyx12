"""Validate the bundled X12 map XML files for structural correctness.

Run as a CI gate to catch the kind of map-file bugs that previously surfaced
only at runtime (see PR #134, issue #135).

Checks:
  1. Every `<element>` references a `data_ele` defined in dataele.xml.
  2. No `<element>` has a C-prefix `data_ele` (those identify composites
     and a `C` data_ele on an `<element>` tag is a mistagged composite).
  3. Every `<valid_codes external="X"/>` references a codeset defined in
     codes.xml.

Exits 0 when clean, 1 when any check fires.
"""

from __future__ import annotations

import pathlib
import sys
from collections.abc import Iterator
from xml.etree.ElementTree import Element

import defusedxml.ElementTree as et

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP_DIR = REPO_ROOT / "pyx12" / "map"

# Files that aren't transaction maps — skip them.
NON_MAPS = {"dataele.xml", "codes.xml", "maps.xml"}


def load_defined_data_elements() -> set[str]:
    root = et.parse(MAP_DIR / "dataele.xml").getroot()
    return {de.get("ele_num") for de in root if de.get("ele_num")}


def load_defined_codesets() -> set[str]:
    root = et.parse(MAP_DIR / "codes.xml").getroot()
    ids: set[str] = set()
    for cs in root.findall("codeset"):
        id_elem = cs.find("id")
        if id_elem is not None and id_elem.text:
            ids.add(id_elem.text.strip())
    return ids


def get_data_ele(node: Element) -> str | None:
    """Read a node's data_ele as either an attribute or a child element."""
    attr = node.get("data_ele")
    if attr:
        return attr
    child = node.find("data_ele")
    if child is not None and child.text:
        return child.text.strip()
    return None


def iter_map_files() -> Iterator[pathlib.Path]:
    for xml_path in sorted(MAP_DIR.glob("*.xml")):
        if xml_path.name in NON_MAPS:
            continue
        yield xml_path


def check_map(
    xml_path: pathlib.Path,
    defined_eles: set[str],
    defined_codesets: set[str],
) -> list[str]:
    findings: list[str] = []
    try:
        tree = et.parse(xml_path)
    except Exception as e:  # pragma: no cover — XML errors at parse time
        return [f"failed to parse: {e}"]

    for node in tree.iter():
        if node.tag == "element":
            de = get_data_ele(node)
            if de is None:
                continue
            xid = node.get("xid", "?")
            if de.startswith("C"):
                findings.append(
                    f"<element xid={xid!r}> has data_ele={de!r}; "
                    f"the C-prefix is reserved for composites — likely mistagged "
                    f"(should be <composite>)"
                )
            elif de not in defined_eles:
                findings.append(
                    f"<element xid={xid!r}> references undefined data_ele={de!r} "
                    f"(not in dataele.xml)"
                )

        elif node.tag == "valid_codes":
            ext = node.get("external")
            if ext and ext not in defined_codesets:
                findings.append(
                    f"<valid_codes external={ext!r}/> references unknown codeset (not in codes.xml)"
                )

    return findings


def main() -> int:
    defined_eles = load_defined_data_elements()
    defined_codesets = load_defined_codesets()

    print(
        f"check_maps: scanning {MAP_DIR.relative_to(REPO_ROOT)} "
        f"against {len(defined_eles)} data elements and "
        f"{len(defined_codesets)} codesets"
    )

    failed_files: dict[str, list[str]] = {}
    file_count = 0
    for xml_path in iter_map_files():
        file_count += 1
        findings = check_map(xml_path, defined_eles, defined_codesets)
        if findings:
            failed_files[xml_path.name] = findings

    if not failed_files:
        print(f"OK: {file_count} map files clean.")
        return 0

    total = sum(len(v) for v in failed_files.values())
    print(f"\nFAIL: {total} finding(s) across {len(failed_files)} of {file_count} files:\n")
    for fname, findings in sorted(failed_files.items()):
        print(f"--- {fname} ---")
        for f in findings:
            print(f"  {f}")
        print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
