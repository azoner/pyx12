# Pyx12

[![Build Status](https://github.com/azoner/pyx12/actions/workflows/main.yml/badge.svg)](https://github.com/azoner/pyx12/actions/workflows/main.yml)


Pyx12 is a HIPAA X12 document parser, validator and converter.  It reads an ANSI X12 data file and validates it against a representation of the X12 Implementation Guidelines.  By default, it creates a 997 response for 4010 and a 999 response for 5010. It can create an HTML representation of the X12 document and can translate to and from an XML representation of the data file. 

# Usage

As a command line X12 validator

    x12valid.exe <filename>

Fixes common X12 structural errors.  Can add or remove line breaks.  Can fix loop and segment counting.

    x12norm.exe --fix --eol <filename>

# Code Examples

    Iterate over a loop.  Alter children. Show changes
```python
    src = pyx12.x12context.X12ContextReader(param, errh, fd_in)
    for datatree in src.iter_segments('2300'):
        # do something with a 2300 claim loop
        # we have access to the 2300 loop and all its children
        for loop2400 in datatree.select('2400'):
            print(loop2400.get_value('SV101'))
            # update something
            loop2400.set_value('SV102', 'xx')
            # delete something
            if loop2400.exists('PWK'):
                loop2400.delete('PWK')
        # iterate over all the child segments
        for seg_node in datatree.iterate_segments():
            print(seg_node.format())
```

# Install

    uv pip install pyx12

# Contributing

The most useful contributions are **new implementation-guide maps** —
either upgrading an existing 4010 map to its 5010 counterpart, or adding
support for an X12 transaction pyx12 doesn't yet cover. Pyx12's design
already handles the engine; the bottleneck is map coverage.

## Where the maps live

XML maps live under `pyx12/map/`, one file per (transaction, version)
pair, named like `<transaction>.<version>.<X-number>[.A<n>].xml` —
e.g. `834.4010.X095.A1.xml`, `837.5010.X222.A1.xml`. The index that
pyx12 consults at runtime is `pyx12/map/maps.xml`; each entry binds a
`(vriic, fic[, tspc])` triple to a map filename:

| Name                                             | Abbreviation | X12 Element |
| :----------------------------------------------- | :----------- | :---------- |
| Interchange Control Version Number               | ICVN         | ISA12       |
| Version / Release / Industry Identifier Code     | VRIIC        | GS08        |
| Functional Identifier Code                       | FIC          | GS01        |
| Transaction Set Purpose Code (used only for 278) | TSPC         | BHT02       |

## Converting a 4010 map to 5010

Several 4010 maps don't yet have 5010 siblings — the candidates are
listed in the commented-out block in `maps.xml` (270/271 eligibility,
276/277 claim status, 277U, 278 services review, 837D dental, 841). To
add one:

1. Get the 5010 implementation guide for the transaction from
   [X12.org](https://x12.org/products) or its HIPAA companion guide.
2. Copy the existing 4010 map as a starting point — `cp
   pyx12/map/270.4010.X092.A1.xml pyx12/map/270.5010.X279.A1.xml` (the
   X-number changes between versions).
3. Walk the IG diff and apply structural changes: new loops, new
   segments, renamed elements, added or removed code values, changed
   `usage` flags, changed `max_use`, changed `repeat`, changed syntax
   rules. The 834.4010 ↔ 834.5010 pair is a good reference for the
   typical scope of changes.
4. Update the `<valid_codes>` lists from the 5010 code list. Many
   external-code references (`<external>`) stay pointed at the same
   bundled list in `codes.xml` but the lists themselves may need
   refreshing — see the commit history for `codes.xml` for the pattern.
5. Register the new file under the `<version icvn="00501">` block in
   `maps.xml`:

   ```xml
   <map vriic="005010X279A1" fic="HS" abbr="270">270.5010.X279.A1.xml</map>
   ```
6. Add a fixture and a test. Tests live under `pyx12/test/`; the
   simplest pattern is a `test_x12n_document.py` entry that runs
   `x12n_document` against a sample file from the IG and compares the
   997/999 output, or a focused `test_map_if_load.py` entry that just
   confirms the map parses cleanly.

## Adding a new X12 IG

The same shape applies — pyx12 is HIPAA-focused but the map engine is
transaction-agnostic. Drop a new XML map into `pyx12/map/`, register it
in `maps.xml` with the right `(icvn, vriic, fic[, tspc])`, and you're
in. If the transaction uses code lists that aren't already bundled,
add them under `<codeset>` blocks in `codes.xml` and reference them
from your map's `<external>` elements.

## Running the project

```bash
# Set up the dev environment
uv sync --extra dev

# Tests
uv run pytest

# Type check
uv run mypy

# Format & sort imports
uv run ruff format pyx12/
uv run ruff check --select I --fix pyx12/
```

A green `pytest` and `mypy --strict` run is required for CI to pass.
PRs welcome via [github.com/azoner/pyx12](https://github.com/azoner/pyx12).

# Licensing

Pyx12 uses a BSD license. The full license text is included with the source code for the package. 
