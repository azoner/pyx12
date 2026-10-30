# Security policy

## Reporting a vulnerability

Report vulnerabilities privately through GitHub:
[Report a vulnerability](https://github.com/azoner/pyx12/security/advisories/new).
Please do not open a public issue for them.

Never include real PHI in a report. Reproduce with synthetic X12 data.

We acknowledge reports within 7 days, and aim to release a fix or publish an advisory within
90 days. We coordinate the disclosure date with the reporter.

## Supported versions

| Version | Security fixes |
|---------|----------------|
| 4.x     | Yes            |
| < 4.0   | No             |

## Scope

pyx12 validates untrusted X12 input, so rejecting malformed data is its normal job. Report
these privately:

- code execution, or reading or writing files outside what the caller asked for
- XML entity or DTD attacks on map loading
- PHI from the input leaking into places it should not, such as another file's output
- small inputs that consume CPU or memory far out of proportion to their size

Report these as ordinary public issues or pull requests:

- crashes or uncaught exceptions on malformed X12, where the only effect is that the one file
  fails to process
- wrong or missing validation errors in 997 / 999 / TA1 output
