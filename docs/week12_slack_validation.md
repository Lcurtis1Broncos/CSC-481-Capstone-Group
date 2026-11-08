# Week 12: Bounded slack recovery and validation

**Reporting period:** November 2 - November 8, 2026

## Original expectations

Use the existing [Week 8 manifest](../reports/evidence/week8/w8_slack_payload_manifest.json).
It records the controlled payload before this week's recovery, rather than
deriving expected values from recovered output.

| Field | Recorded expectation |
|---|---|
| Host | Testfile.docx, record 41 |
| Normal content size | 13,437 bytes |
| Allocated size | 16,384 bytes |
| Calculated final-cluster slack | Offset 16,049,277; length 2,947 bytes |
| Payload | TEAM3_SLACK_TEST_20261008; UTF-8, no BOM or newline |
| Payload location | First 25 bytes of that slack region |
| Payload SHA-256 | `3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2` |
| Working image SHA-256 | `D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7` |

The remaining 2,922 slack bytes are not part of this known payload. Their
contents are not classified as empty or benign by this recovery.

## Manual recovery and verification

Jeff inspected record 41 November 3, then used PowerShell November 4 to open
the image read-only, seek to the manifest offset, and read exactly 25 bytes.
The output file was created with CreateNew, refusing an existing destination.
Its displayed text matched the known marker. On November 6, its file hash
was checked during documentation/implementation work and matched the manifest.
The manual screenshot is evidence of extraction/text, not a whole-image hash
comparison; source preservation is additionally checked by the integrated run.

## Recovery-support change

`locate_slack_payload` calls the existing strict `locate_stream` to validate
geometry, MFT coverage, USA fixups, stream flags, data runs, and volume bounds.
It then selects only a positive-length byte range fully inside calculated
final-cluster slack. No arbitrary absolute disk offset is accepted.

`--slack-length 25` selects the first 25 bytes of slack. `--slack-offset N`
is relative to slack start, not to the image or the normal document content.
Omitting the slack options preserves normal stream recovery behavior.
Reports retain host size and full slack range separately from payload size.

Resident, empty, cluster-aligned, compressed, sparse, encrypted, extension,
and fragmented-MFT cases remain subject to the existing refusal boundaries.
Fragmented ordinary file contents are supported, with slack mapped to the
last logical cluster rather than assumed adjacent to the first extent.

## Regression tests

Eight slack tests extend the existing 56-test suite to **64 passing tests**.
The November 6 agent-run log shows 64 passed in 2.656 seconds with no skips
or failures. Tests cover:

- Final-fragment slack location and byte-exact output/source preservation.
- Relative offsets, exact boundary reads, and rejection beyond the slack end.
- Invalid lengths, negative offsets, and files without supported slack.
- PASS/FAIL report expectations and the actual command-line recovery path.
- Refusal of invalid report ranges before creating output/report files.
- Existing output/source overwrite prevention.

[Saved test log](../reports/evidence/week12/w12_automated_tests.txt).
Jeff subsequently ran the expanded suite himself November 6: all 64 tests
passed in 4.741 seconds, with no failures or skips. See his
[command screenshot](../reports/evidence/week12/w12_automated_tests_command.png)
and [summary screenshot](../reports/evidence/week12/w12_automated_tests_summary.png).

## Real-image command

```powershell
py code/ntfs_recovery.py "NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd" --record 41 --slack-length 25 --output reports/evidence/week12/recovered/w12_slack_marker.bin --report reports/evidence/week12/w12_slack_recovery_report.json --expected-length 25 --expected-sha256 3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2 --expected-image-sha256 D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7
```

The output folder must exist, and output/report files must be new. Full-image
hashing before/after takes longer than the small payload read. The saved
[recovery report](../reports/evidence/week12/w12_slack_recovery_report.json)
is the source of actual results. Do not rerun against its existing paths.

## Remaining validation boundaries

This is recovery of a known payload, not automatic hidden-data discovery.
Independent original hashes for the eight baseline files are still missing,
so those content-equality checks remain open even if the known ADS and slack
payload comparisons pass. The new tests do not establish universal NTFS support.
