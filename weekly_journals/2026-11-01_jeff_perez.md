# Weekly Journal - Jeff Perez

**Week:** 11

**Reporting period:** October 26 - November 1, 2026

**Status:** Complete; finalized November 1

## Work completed

- Met with Lucas Monday, October 26 to discuss this week's assignments and
  planned to meet again Friday to share our completed work.
- Used the existing recovery implementation for this week's planned ADS
  validation instead of treating last week's code as new development.
- Inspected MFT record 58 and confirmed hostfile.txt has a 31-byte unnamed
  resident stream and the 36-byte named CapstoneEvidence ADS.
- On October 29, ran a new integrated recovery with the original payload
  length/hash and expected working-image hash. The report returned PASS:
  36 bytes recovered, original ADS hash matched, and image hash unchanged.
- On October 30, repeated recovery with a deliberately incorrect expected
  hash of 64 zeros. The recovered length still matched, but the hash check
  correctly returned false and overall verification was FAIL. The image
  remained unchanged. This was a successful negative test, not a new defect.
- Ran the automated suite October 30. All 56 tests passed in 1.694 seconds,
  with no failures or skips.
- Supplied screenshots and saved JSON recovery reports for the weekly
  evidence. The report now embeds key screenshots directly, following the
  professor's request for visible evidence rather than links alone.

## What I learned

The parser identifying a stream is not the same as verifying recovered
content. I need the correct record and stream name, then the original
expected byte count and hash to check the exported payload.

The report separates two important checks. `hash_match` compares the recovered
payload with the original payload hash. `source_unchanged` compares the disk
image's hash before and after recovery. They answer different questions.

An incorrect hash can fail verification even when the length is correct.
A mismatch does not identify why the bytes differ; it could involve the
expectation, selected stream, corruption, modification, or a recovery problem.

## Problems encountered and resolution

I initially passed recovery options to the metadata-reader command, which
rejected them. Running `ntfs_recovery.py` with those options resolved the
command mix-up. The recovery and regression tests then behaved as expected.
I have no outstanding issues with my portion of this week's work.

## Limitations

These tests validate the existing controlled resident ADS. They do not
establish support for every ADS or NTFS layout, and they do not recover the
slack marker. Original hashes for the eight baseline files are still needed
for independent verification of those recovered file contents.

## Plan for next week

- Begin the planned slack-range and slack recovery validation for November 2 - 8.
- Compare recovered slack payload bytes and hash with the existing manifest.
- Continue preserving the source image and documenting actual test results.

## Supporting evidence

- [Week 11 report with embedded screenshots](../reports/weekly_report_11.md)
- [ADS recovery report, October 29](../reports/evidence/week11/w11_ads_recovery_report.json)
- [Negative-test report, October 30](../reports/evidence/week11/w11_ads_negative_report.json)
- [56 passing tests](../reports/evidence/week11/w11_automated_tests.png)
- [Week 11 meeting minutes: October 26 and 30](../meeting_minutes/2026-10-26.md)
