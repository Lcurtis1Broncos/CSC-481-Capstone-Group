# Demonstration Command Check

The parser and two recovery commands were exercised on November 25, 2026,
against the actual Windows laboratory working image. This checks technical
execution; the presenters' speaking rehearsal and elapsed presentation time
have not yet been confirmed.

| Check | Result |
|---|---|
| Expected working-image SHA-256 before export | Matched |
| Record 41 document and slack metadata | 2,947 slack bytes at offset 16,049,277 |
| Record 58 named ADS | CapstoneEvidence identified |
| ADS recovered length and original hash | Matched, 36 bytes |
| Slack recovered length and original hash | Matched, 25 bytes |
| Source hash after both exports | Matched the before hash |

The [saved comparison](recovery_check.json) records both payload comparisons
and complete source-image hashes. [Parser output](parser_output.txt) records
the metadata view. Outputs were written into a new local directory, outside
the repository, with no changes to the source image. No original-file hash
comparison for the eight baseline files is implied by these marker checks.

The comparison JSON was saved by the PowerShell command check. The fast
recovery commands did not use the integrated Python `--report` option.
See the [demonstration guide](../../../presentation/DEMO_GUIDE.md) for the
speaking sequence, commands, original expectations, and rehearsal checklist.
