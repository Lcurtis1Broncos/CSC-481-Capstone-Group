# Week 10 Team Progress Report

**Reporting period:** October 19–25, 2026

**Team:** Lucas Curtis and Jeff Perez

**Status:** Complete weekly progress record; updated October 24

## Milestone status and plan alignment

Milestone 6, Forensic Recovery and Extractor Implementation, is in progress
on its planned October 19–November 8 schedule. This week's planned outputs
are Jeff's data-location/recovery-support functions and Lucas's extractor
integration/recovery-report format. The full ADS and slack recovery campaigns
remain scheduled for the next two weeks. Jeff's support functions and Lucas's
workflow/report format are delivered locally and on GitHub respectively.
Team 3 completed the automated extractor/report integration October 24,
using the existing support engine and Lucas's workflow/report fields. The
week's support and integration outputs are implemented and tested locally.
The overall milestone remains in progress through November 8; further ADS
and slack validation is still planned.

## Subtasks completed

| Member | Contribution verified this week |
|---|---|
| Lucas | Added the ADS recovery workflow/report template in GitHub commit `3f5339d` on October 20, defining source/host/stream fields, output fields, comparison results, procedure, acceptance checklist, and pass condition. |
| Jeff | Implemented read-only data-location and recovery-support functions for resident and ordinary nonresident streams, protected output creation, shared USA restoration, and actual recovered length/hash reporting. Added 14 regression tests and the controlled-image validation runner. |
| Jeff | Independently decoded first-run locations for three files and documented the implementation, limitations, validation commands, and Lucas integration handoff. |
| Jeff | Personally ran resident/nonresident recovery and overwrite-refusal checks October 22, then ADS recovery and the 45-test suite October 23; supplied screenshots of the results. |
| Team 3 | Completed automated recovery/report integration October 24, including expected/actual comparisons, source before/after hashes, new-output protection, 11 additional tests, and a saved real-image PASS report. |
| Team | Met October 20 to discuss this week's assigned tasks; no issues reported. Met again October 23 to share completed work and prepare the journals and team report. |

The October 24 GitHub fetch confirms Lucas's latest upload remains commit
`3f5339d`, the workflow/report template. The newer implementation and completed
reports are currently local Team 3 work awaiting publication. This team credit
does not claim Lucas independently implemented or executed the new code;
Jeff's personal recovery runs remain credited to Jeff.

The team now also has a [completed ADS recovery report](week10_ads_recovery_report.md),
prepared October 24 using Lucas's report format and Jeff's October 23 recovery
evidence. That report also links the October 24 automated integration run and
its machine-generated result.

## Tests and evidence

### 1. Regression suite

**Method:** Run the existing parser/embedding tests plus the new synthetic
recovery tests. Expected results include exact recovered fixture bytes,
correct partition offsets and logical run order, zero-fill past initialized
size, and refusal of malformed/unsupported inputs and existing outputs.

**Result:** All 45 tests passed on October 21, no skips or failures.
[Saved test output](evidence/week10/w10_automated_tests.txt).
Jeff reran the suite October 23: **45 tests passed in 0.297 seconds**, with
no skips or failures. Screenshots show the
[command and initial tests](evidence/week10/w10_automated_tests_command.png)
and [remaining tests and final summary](evidence/week10/w10_automated_tests_summary.png).
The new resident fixture crosses a sector tail, proving USA restoration
recovers original bytes instead of returning the on-disk fixup marker.

### 2. Three-file location cross-check

**Method:** Independently read raw record headers/mapping pairs without the
recovery/parser offset helpers. Decode the first LCN and apply the known
partition/cluster geometry.

**Observed offsets:** Test2.txt 16,203,776; Testfile.docx 16,035,840;
SunflowerTest.jpg 16,093,184. Compare with the support function's extents in
the [real-image report](evidence/week10/w10_recovery_validation.json).
[Detailed method and raw mapping pairs](../docs/week10_recovery_support.md).

### 3. Real-image recovery validation

**Method:** Verify the known ADS/slack working image hash, recover the eight
baseline files plus the named ADS to new separate output files, compare known
sizes and the ADS original hash, check the documented slack range, and hash
the source again to verify preservation.

The runner saves actual results and their limits in the
[validation report](evidence/week10/w10_recovery_validation.json). Baseline
file hashes are measured output hashes only: original hashes have not been
supplied, so original-content hash equality is not yet established. The ADS
manifest supplies an independent expected 36-byte length and original hash.
The slack check covers the location/range only, not slack payload extraction.

**Result, October 21:** All eight recovered lengths matched; the 36-byte ADS
matched its original SHA-256; the slack range matched; the source image's
before/after SHA-256 values were identical and matched its recorded hash.
The separate three-file first-run offset cross-check also agreed with the
saved extents. This does not close the missing original hashes for the eight
baseline files.

### 4. Jeff's hands-on recovery and safety checks, October 22–23

**Inputs:** The same controlled working image; records 38, 41, and 58.
**Method:** Run the support utility with a new `--output` path for each stream.
Repeat record 41's command with the same output path to test overwrite refusal.

| Test | Expected result | Observed result and demo screenshot |
|---|---|---|
| Resident Test.txt, record 38 | Export 83 logical bytes from the restored MFT record. | Passed: [83-byte recovery](evidence/week10/w10_resident_recovery.png). |
| Nonresident Testfile.docx, record 41 | Export 13,437 logical bytes, not its 16,384-byte allocation. | Passed: [13,437-byte recovery](evidence/week10/w10_nonresident_recovery.png); 2,947 slack bytes excluded. |
| Reuse the document output filename | Refuse to overwrite the existing output. | Passed: [expected destination refusal](evidence/week10/w10_overwrite_refusal.png). |
| Named CapstoneEvidence ADS, record 58 | Recover 36 bytes; match the original payload SHA-256. | Passed: [ADS recovery and hash](evidence/week10/w10_ads_recovery.png). |

Expected and observed ADS SHA-256:
`E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E`.
The screenshots establish actual exports and the reported values. The
October 21 before/after image hashes separately establish source preservation
for that validation run; the screenshots alone are not a new whole-image hash
comparison for October 22–23.

### 5. Automated extractor/report integration, October 24

**Method:** Extend the same recovery command with `--report`, original
expected payload length/hash, and the recorded expected image hash. The
integrated function locates and recovers the selected stream, hashes the
full image before/after, saves actual and expected results, and sets the
verification status. New output and report paths are required.

**Result:** The real-image run recovered 36 bytes from record 58's named
CapstoneEvidence stream. Payload length and SHA-256 matched the original
manifest; the before/after source hashes both matched the expected working
image hash. The generated report records **PASS**, with no errors:
[automated ADS report](evidence/week10/w10_integrated_ads_report.json).

**Regression:** All **56 tests passed in 2.881 seconds** on October 24, with
no failures or skips. The 11 new integration tests cover matching/mismatched
expectations, missing originals (NOT_VERIFIED rather than PASS), a changed or
wrong source image hash, error reporting, path collisions/overwrite refusal,
and actual CLI exit codes. See [saved test output](evidence/week10/w10_integrated_tests.txt).
Jeff reran the expanded suite October 24: **56 tests passed in 1.708 seconds**,
with no failures or skips. Screenshots show the
[command and initial results](evidence/week10/w10_integrated_tests_command.png)
and [integration tests and final summary](evidence/week10/w10_integrated_tests_summary.png).
The earlier screenshots remain evidence of the separate October 23 45-test run.

## Lessons from implementation and testing

- Resident file content must be recovered after restoring NTFS sector-tail
  fixups, not copied blindly from a raw contiguous byte range.
- Nonresident recovery follows logical run order and stops at logical EOF;
  allocated cluster slack is not part of ordinary file content.
- Initialized length matters: uninitialized logical bytes must be returned as
  zeros instead of exposing stale allocated disk bytes.
- A measured recovered hash alone does not prove correctness; compare it with
  an independently recorded original hash and expected byte count.

These findings are reflected in the members' weekly journals and the saved
implementation/test evidence.

## Remaining work and submission

- The planned Week 10 support and automated reporting implementation is now
  complete locally, with the real-image and regression results above. Continue
  broader ADS validation October 26–November 1 and slack recovery November 2–8.
- Both journals, Friday's meeting record, and the demonstration screenshots
  are prepared locally for review.
- The completed ADS report records the observed 36-byte payload and matching
  original hash using Lucas's template; the test execution is credited to Jeff.
- The subsequent automated report, 56-test log, and Jeff's updated command
  and result screenshots document the October 24 integration and regression.
- Commit/push each member's genuine contributions and have the team leader
  submit the repository URL by October 25. Local documentation completion is
  not confirmation that GitHub publication or the course submission occurred.

Original hashes of the eight baseline files are a remaining Milestone 6
validation item. The existing known ADS hash already supports the first
payload comparison; no new ADS or creation script is needed.

## Team records

- [Jeff's journal](../weekly_journals/2026-10-25_jeff_perez.md)
- [Lucas's journal](../weekly_journals/2026-10-25_lucas_curtis.md)
- [October 20 planning meeting](../meeting_minutes/2026-10-20.md)
- [October 23 progress meeting](../meeting_minutes/2026-10-23.md)
