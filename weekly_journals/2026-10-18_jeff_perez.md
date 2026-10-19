# Weekly Journal - Jeff Perez

**Week:** 9
**Reporting period:** October 12 - October 18, 2026
**Status:** Complete

## Work completed

- Attended Tuesday's October 13 planning meeting at 7:30 p.m. with Lucas
  and discussed our upcoming work and planned follow-up.
- Compared the semester plan with the merged code and evidence to identify
  remaining validation and documentation tasks.
- Followed up on the midterm package submitted October 11 with additional
  validation and documentation.
- Reran the parser against records 41 and 58 in the ADS/slack working image.
  The file metadata, data run, slack location, and 36-byte named ADS matched
  the documented results.
- Independently checked record 58's resident DATA headers using PowerShell.
  The unnamed 31-byte stream and named 36-byte stream matched the parser
  and Lucas's earlier VM evidence.
- Consolidated the parser design, field map, validation checklist, and limits
  into a standalone reference.
- Updated the central evidence log to include the known-file, ADS, and
  ADS/slack image versions and their recorded integrity information.
- Clarified the semester plan's ADS deliverable as Lucas's documented manual
  PowerShell procedure.
- Retained the original ADS image, payload manifest, and manual instructions.
  No new ADS host or image was created.
- Reran the active parser/embedding suite: all 31 tests passed
  with no skips or failures.
- Captured the full test run showing 31 tests, `OK`, and a runtime of
  0.123 seconds.
- Captured two parser screenshots showing the command, record 41's file
  sizes/data run/slack range, and record 58's host name and named ADS.
- Met with Lucas on Saturday, October 17 after rescheduling Friday's meeting.
  We reviewed what remained for this week's submission and planned next
  week's tasks. We reported no issues; his exact file-size listing was pending
  at that meeting.
- Received Lucas's VM exact-size listing October 18 and compared all eight
  names and byte lengths with the parser's recorded logical sizes. All matched.
  Added the source screenshot and comparison table to close that validation gap.

## What I learned

Independent validation needs a separate comparison, not just the same parser
producing the same values twice. Reading the resident DATA headers directly
and comparing them with the VM stream listing provides another check on the
reported names and sizes.

The manual ADS procedure and its source evidence provide a clear basis for
checking the parser's metadata now and validating recovered contents later.

## Problems encountered and resolution

The review identified gaps between planned outputs and the files in the
repository. I consolidated the design and evidence records and adjusted the
ADS output in the plan to match the retained manual procedure.

Our semester plan set aside October 12 - 18 for midterm preparation, but
October 12 turned out to be the deadline. Since we submitted October 11,
we used this week for follow-up validation and planning next week's tasks.

## Limitations

No payload extractor or recovered ADS hash validation was completed this week.
The current parser's fragmented-MFT and extension-record limitations remain.
The eight-file comparison verifies names and logical sizes, not file-content hashes.

## Plan for next week

- Begin read-only content-location and recovery-support work for Milestone 6.
- Compare recovered payload hashes with the source manifests when extraction
  becomes available.

## Supporting evidence

- [Week 9 validation](../docs/week9_validation.md)
- [Design and limitations](../docs/parser_design_and_limitations.md)
- [Manual ADS workflow](../docs/ads_creation_workflow.md)
- [Meeting minutes](../meeting_minutes/2026-10-13.md)
