---
name: reviewer-writing
description: Write PR descriptions, GitHub issue and PR comments, release notes, and substantial commit messages so a human reader gets the point in seconds. Use whenever creating or updating a pull request, commenting on an issue or PR, drafting release notes, or writing a commit message longer than a line. Answer first, reader's job, risk, evidence linked not pasted.
---

# Writing for human reviewers

**Why:** PR and issue text gets so dense with counts, test lists and internal labels that
reviewers can't find the point. Detail is not the problem; detail in the wrong place is. Every
piece of text has one reader and one job.

## Where each kind of content goes

| Place | Reader | Job | Detail level |
|---|---|---|---|
| **PR description** | the maintainer reviewing it, today | the decision: what changed, what to check, the risk | short -- the template below |
| **Issue comment** | the reporter, and anyone who finds the issue later | the outcome: fixed or not, in which release, what to do | 6 lines or fewer |
| **Release notes** (`gh release create`) | users deciding whether to upgrade | what changed for them, anything that breaks | one line per change |
| **Commit message** | a future engineer reading `git log` | the technical record: what and why, mechanism, verification summary | as dense as needed |
| **Repo files and CI** (tests, fixtures in `pyx12/test/`, Actions runs) | anyone verifying a claim | the evidence | complete |

Write each fact once, in the place it belongs, and link from the others. Do not paste the same
evidence into the commit, the PR and the issue. PRs are squash-merged, so the commit message
becomes the `master` history -- that is where the technical detail lives.

## PR template

```markdown
**<One-line title restated as the outcome.>** <1-2 plain sentences: what changed and why.>

**Your job:** <No action -- record of X | Check: … | Decide: … | Try: <command> on <file>>
**Risk:** <one line: what could go wrong and how it is undone. "None -- docs only" is a fine answer.>
**Evidence:** <conclusions with links, e.g. "608 tests pass; ack output unchanged for every fixture -- see the commit message.">
```

Add at most 5 bullets beneath if the reviewer genuinely needs them (e.g. behavior that changed
for users). Anything longer goes into the commit message or a file and is linked. Use `Closes #N`
so the issue closes on merge. Keep the attribution footer the system asks for.

## Issue comment template

```markdown
**<Outcome in one line>** -- fixed in #N, released in vX.Y.Z (or: not yet released).
<1-2 lines: what was wrong and what changed, in the reporter's terms.>
**Next:** <what the reporter does: upgrade, retest, or nothing>.
```

Write for someone who may not know the codebase. Thank external reporters once, briefly.

## Rules

1. **Answer first.** The first 3 lines must stand alone. A reader who stops there knows what
   happened and whether to approve.
2. **Name the reader's job** explicitly -- don't make them infer it.
3. **Conclusions in prose, data in files.** "608 tests pass" with a link, not the test list.
   Per-test inventories and fixture diffs belong in the commit message or the CI log.
4. **Gloss internal labels.** Say the thing, then the ID: "the 999 error for a missing required
   element (IK4 code 1)", "the JSON error output (issue #50)". Never "per #50" alone.
5. **One idea per bullet, plain words.** No stacked qualifiers; put caveats once, at the end
   ("Not tested: 4010 maps").
6. **Numbers: only the ones that decide something.** "Ack output unchanged; 6 JSON fixtures gain
   one entry each" -- not every count from every test class.
7. **Prefer the user's vocabulary** to the code's ("the XML output", not "the
   `x12xml_simple.seg` writer stack").

## Worked example (PR #181)

**Before** (~40 lines): a paragraph on the invariant, a section listing ten new test names by
class, a section listing four files changed, and a four-item test plan with running test totals.

**After:**

> **Error codes now always attach at the right level of the error tree.** New tests check that
> element and composite codes (`ELE_*`, `COMP_*`) land on elements and segment codes (`SEG_*`)
> land on segments. The one place that broke this stored a bare X12 `"8"` on the segment; it
> now uses a named code, `SEG_8_HAS_DATA_ELEMENT_ERRORS`.
>
> **Your job:** no action -- record of the new invariant.
> **Risk:** low -- 997/999 output is unchanged; the ack still reports `8`.
> **Evidence:** 597 tests pass; mypy strict and ruff clean. The new tests are listed in the
> commit message.

Same facts, a quarter of the length; nothing was lost -- it moved to where it is read.

## Checklist before posting

- [ ] Could the reader act after reading only the first 3 lines?
- [ ] Is the reader's job stated?
- [ ] Is every internal label or issue number explained in plain words?
- [ ] Is any evidence pasted that the commit message or CI already holds? Link it instead.
- [ ] PR: summary + 5 bullets or fewer? Issue comment: 6 lines or fewer?
