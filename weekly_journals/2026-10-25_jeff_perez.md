# Weekly Journal - Jeff Perez

**Week:** 10
**Reporting period:** October 19 - October 25, 2026
**Status:** Complete; updated October 24

## Work completed

- Met with Lucas on October 20 to discuss our assigned tasks for the week.
  We reported no issues and planned to meet again Friday at 7:00 p.m.
- Worked with guided assistance on the data-location and read-only recovery
  support for Milestone 6. The new support locates file content, recovers
  resident and ordinary nonresident streams, and reports recovered sizes
  and SHA-256 hashes.
- Reviewed the changes through short lessons Wednesday through Friday so I
  could connect the code's output to the work assigned in our semester plan.
- On Wednesday, located Test.txt in record 38 and Testfile.docx in record 41.
  Compared their resident/nonresident status and learned to distinguish the
  MFT record's location from the location of the file's actual content.
- On Thursday, recovered Test.txt to a separate file containing 83 bytes.
  Recovered Testfile.docx to a separate file containing 13,437 bytes, rather
  than including its 2,947 bytes of final-cluster slack.
- Repeated the Word document recovery command with the same output filename.
  The tool refused to overwrite the existing output, as expected.
- On Friday, recovered the CapstoneEvidence ADS from hostfile.txt in record
  58. Its recovered length was 36 bytes, and its SHA-256 matched Lucas's
  original payload manifest.
- Ran the automated test suite myself on October 23. All 45 tests passed in
  0.297 seconds, with no skips or failures.
- Captured screenshots of the location output, file recoveries, overwrite
  refusal, ADS recovery, and automated test results for documentation.
- Met with Lucas on Friday, October 23. We shared the work we completed
  during the week and discussed finishing our journals and weekly report.
- The team's October 24 follow-up completed automated recovery/report
  integration. The saved report verified the ADS length/hash and unchanged
  source image; the expanded suite passed all 56 tests. This team follow-up
  is separate from the personal command runs documented above.
- Reran the expanded test suite myself October 24 and captured the command
  and final results. All 56 tests passed in 1.708 seconds, with no failures
  or skips.

## What I learned

Before this week, our parser showed file information and content locations.
The new recovery support reads the actual content and saves it separately.
Resident content is stored inside the MFT record, while nonresident content
is located by following data runs to clusters elsewhere in the image.

I learned why recovery uses the logical file size instead of copying all
allocated space. For Testfile.docx, the file contains 13,437 bytes even though
it occupies 16,384 allocated bytes. The remaining 2,947 bytes are slack and
should not be included in the recovered document.

We also covered restoring sector-tail bytes in memory before reading
resident content. This does not write changes to the source image. Comparing
the ADS's recovered size and hash with Lucas's original values provided a
stronger check than matching its size alone.

## Problems encountered and resolution

The recovery commands and automated tests I ran completed as expected. The
existing-output error was an intentional safety test, not an unresolved bug.

## Limitations

The recovered ADS matched its original payload hash. The original hashes
for the eight baseline files have not been supplied, so matching their sizes
does not yet establish original-content hash matches.

The support does not recover deleted files or handle fragmented MFT storage,
attribute-list extensions, or compressed, sparse, or encrypted streams.
Slack-range calculation is available, but this week's lesson did not recover
the hidden slack payload.

## Plan for next week

- Continue ADS recovery validation according to the semester plan.
- Review the extractor/report integration with Lucas and compare actual
  recovered results with the original payload manifest.

## Supporting evidence

- [Week 10 recovery support](../docs/week10_recovery_support.md)
- [Week 10 team report](../reports/weekly_report_10.md)
- [Recovery validation results](../reports/evidence/week10/w10_recovery_validation.json)
- [October 21 automated test log](../reports/evidence/week10/w10_automated_tests.txt)
- [October 20 meeting minutes](../meeting_minutes/2026-10-20.md)
- [October 23 meeting minutes](../meeting_minutes/2026-10-23.md)
- [Resident recovery](../reports/evidence/week10/w10_resident_recovery.png)
- [Nonresident recovery](../reports/evidence/week10/w10_nonresident_recovery.png)
- [Overwrite refusal](../reports/evidence/week10/w10_overwrite_refusal.png)
- [ADS recovery](../reports/evidence/week10/w10_ads_recovery.png)
- [October 23 automated test results](../reports/evidence/week10/w10_automated_tests_summary.png)
- [Team automated ADS report, October 24](../reports/evidence/week10/w10_integrated_ads_report.json)
- [Team integration regression log, October 24](../reports/evidence/week10/w10_integrated_tests.txt)
- [My expanded-suite command, October 24](../reports/evidence/week10/w10_integrated_tests_command.png)
- [My 56-test result, October 24](../reports/evidence/week10/w10_integrated_tests_summary.png)

The October 23 personal test run is shown in my screenshots; the saved text
log above records the earlier October 21 run.
