# Weekly Journal - Lucas Curtis

**Week:** 9
**Reporting period:** October 12 - October 18, 2026
**Status:** Complete

## Work completed

- Attended the Tuesday, October 13 planning meeting at 7:30 p.m. with Jeff
  and discussed our work for the week.
- Met with Jeff on Saturday, October 17 after rescheduling Friday's meeting.
  We reviewed the remaining weekly work and submission preparation and
  discussed next week's tasks. No issues were raised during the meeting.
- Ran PowerShell in the VirtualBox guest to list the original eight test
  files with their full names and exact byte sizes:

```powershell
Get-ChildItem -LiteralPath 'D:\' -File | Select-Object Name, Length
```

- Sent the output screenshot to Jeff. It was received October 18 and used
  to compare the VM file sizes with the parser's recorded logical sizes.
- Provided the independent source evidence for the exact-size comparison.
  Jeff completed the comparison, and all eight filenames and byte sizes matched.

The midterm report was submitted October 11. We had planned to use this week
for midterm preparation, but October 12 was the deadline. We used the week
for follow-up validation and discussing the next phase. Our original manual
ADS workflow and controlled image remain unchanged.

## What I learned

File Explorer displays rounded KB values, while PowerShell's `Length` field
reports the exact size in bytes. Exact values allow a direct comparison
with the parser's logical file sizes. One command lists all eight files;
it does not need to be run separately for each file.

Matching names and sizes checks the parser's metadata results. It does not
establish that file contents or recovered payload hashes match; those are
separate recovery tests.

## Problems encountered and resolution

No issues were raised during our Saturday review. The outstanding exact-size
evidence was supplied October 18, allowing Jeff to finish the comparison.

## Plan for next week

- Begin the assigned read-only extractor integration and recovery-report
  workflow for October 19 - 25.
- Coordinate ADS recovery work with Jeff's content-location functions.
- Keep the original payload markers and hashes available for later comparison
  with recovered bytes.

## Supporting evidence

- [VM exact file sizes](../reports/evidence/week9/w9_vm_exact_file_sizes.png)
- [Eight-file size comparison](../docs/week6_known_file_manifest.md#exact-size-comparison-completed-october-18)
- [Week 9 report](../reports/weekly_report_09.md)
- [Week 9 meeting minutes](../meeting_minutes/2026-10-13.md)
