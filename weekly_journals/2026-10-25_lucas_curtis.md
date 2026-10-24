# Weekly Journal - Lucas Curtis

**Week:** 10
**Reporting period:** October 19 - October 25, 2026
**Status:** Complete

## Work completed

- Met with Jeff on October 20 to discuss our tasks for the week and the
  start of the forensic recovery phase. We reported no issues and planned
  to meet again Friday at 7:00 p.m.
- Created and uploaded the ADS recovery workflow and recovery-report
  template to GitHub on October 20 in commit `3f5339d`.
- Included fields for the source image and hash, host filename, MFT record,
  ADS stream name, expected payload length/hash, and actual recovered
  output length/hash.
- Documented the recovery procedure, verification results, and a section
  for recording problems and observations.
- Added acceptance criteria requiring a separate output file and matching
  recovered byte count and SHA-256 before reporting a passing result.
- Met with Jeff on Friday, October 23. We shared our completed work and
  discussed finishing the weekly journals and team report.

## What I learned

A recovery report needs to identify the source image, host record, and
specific stream so the result can be traced back to the correct input.
Expected values come from the original payload manifest, while actual values
come from the recovered output. Matching the length alone is not enough;
the recovered hash must also match the original payload hash.

The report format keeps the recovery procedure, results, and any problems
together so another person can follow the steps and review the evidence.

## Problems encountered and remaining work

No issues were reported during our October 20 planning meeting. My uploaded
document establishes the workflow and report format; it is not a completed
recovery test report or a separate extractor implementation.

Jeff's recovery-support code and test results are documented in the team
report. Team 3 subsequently added automated reporting on October 24 using
the workflow and report fields I contributed. That integration is recorded
as a team deliverable, not as an independent implementation or test run by me.

## Plan for next week

- Review the team's integrated recovery/report command and generated results.
- Run the ADS recovery workflow and record the expected and actual payload
  lengths/hashes using the report format.
- Coordinate the planned October 26 - November 1 ADS validation with Jeff.

## Supporting evidence

- [ADS recovery workflow and report template](../docs/ADS%20Recovery%20Workflow.md)
- [GitHub contribution](https://github.com/Lcurtis1Broncos/CSC-481-Capstone-Group/commit/3f5339d)
- [Week 10 team report](../reports/weekly_report_10.md)
- [Recovery-support integration handoff](../docs/week10_recovery_support.md)
- [October 20 meeting minutes](../meeting_minutes/2026-10-20.md)
- [October 23 meeting minutes](../meeting_minutes/2026-10-23.md)
