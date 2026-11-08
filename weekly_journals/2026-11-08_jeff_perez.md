# Weekly Journal - Jeff Perez

**Week:** 12

**Reporting period:** November 2 - November 8, 2026

**Status:** Complete; finalized November 8

## Work completed

- Met with Lucas November 2 at 7:30 p.m. to review this week's assigned
  slack-space recovery and validation tasks.
- Inspected record 41 November 3 and distinguished Testfile.docx's 13,437
  content bytes from its 16,384 allocated bytes and 2,947 slack bytes.
- Located slack at absolute image offset 16,049,277 and checked the original
  manifest's 25-byte payload length.
- Used PowerShell November 4 to open the image read-only and recover exactly
  25 bytes into a new separate file. The output displayed the expected marker,
  TEAM3_SLACK_TEST_20261008. The command used new-file creation to prevent
  overwriting an existing output.
- Continued implementation and verification with guided assistance November 6.
  Bounded slack selection was added to the existing recovery/report tool so
  it calculates the location from the host metadata and validates the range.
- The saved manual output was hashed during that follow-up and matched the
  original payload manifest. The integrated recovery also returned PASS for
  the 25-byte payload and confirmed identical before/after source image hashes.
- The expanded agent-run suite passed all 64 tests, including eight new slack
  cases. These results are recorded separately from my personal manual run.
- Reran the full suite myself November 6 and captured the command and summary.
  All 64 tests passed in 4.741 seconds, with no failures or skips.
- Supplied location/recovery screenshots and began the weekly evidence and
  report package with screenshots embedded directly.
- Displayed the saved integrated recovery report and supplied its screenshot,
  showing 25 recovered bytes, matching original hash, unchanged source, and PASS.
- Met with Lucas November 7 at 7:30 p.m. for the follow-up meeting. We shared
  our tasks and went over the work completed during the week.

## What I learned

Recovering the Word document and recovering a marker in its slack are separate
operations. The document export stops at 13,437 bytes. The known marker begins
at slack offset 16,049,277 and occupies 25 bytes, not the whole 2,947-byte range.

The original manifest supplies the expected marker size and hash. Seeing the
expected text does not replace checking its exact-byte hash. The program also
needs to validate requested ranges and preserve the source image while creating
only new output files.

## Problems encountered and resolution

The manual recovery produced the expected 25-byte marker. The remaining
implementation gap was that normal stream recovery intentionally excludes
slack. Explicit bounded slack selection was added and tested rather than
changing ordinary file recovery to include extra allocated bytes.

## Limitations

This is recovery of a known payload, not discovery of unknown hidden content.
The rest of the slack region has not been classified by this test. The
original hashes of the eight baseline files remain needed for independent
verification of their recovered contents.

## Plan for next week

- Begin the planned full test campaign and record pass/fail results and limits.
- Retain the image hashes, payload hashes, screenshots, and recovery reports
  needed for the final forensic documentation.

## Supporting evidence

- [Weekly report](../reports/weekly_report_12.md)
- [Slack validation reference](../docs/week12_slack_validation.md)
- [Original slack manifest](../reports/evidence/week8/w8_slack_payload_manifest.json)
- [Manual marker recovery](../reports/evidence/week12/w12_manual_marker_recovery.png)
- [Integrated slack recovery report](../reports/evidence/week12/w12_slack_recovery_report.json)
- [Integrated PASS screenshot](../reports/evidence/week12/w12_slack_recovery_pass.png)
- [Regression test log](../reports/evidence/week12/w12_automated_tests.txt)
- [My regression command](../reports/evidence/week12/w12_automated_tests_command.png)
- [My 64-test result](../reports/evidence/week12/w12_automated_tests_summary.png)
- [Weekly meeting minutes](../meeting_minutes/2026-11-02.md)
