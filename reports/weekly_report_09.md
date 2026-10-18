# Week 9 Team Progress Report

**Reporting period:** October 12 - October 18, 2026
**Team:** Lucas Curtis and Jeff Perez
**Status:** Complete

## Milestone status

Milestone 5's midterm package was completed and submitted on October 11,
2026. The semester plan had allocated October 12 - 18 for midterm preparation,
but October 12 was the deadline rather than the start of that work. With the
package already submitted, the team used this week for follow-up validation,
documentation, and planning the next phase. The midterm package and Week 8
work are merged through PR #17.

This week's completed subtasks provide follow-up verification: repeat parser
validation, an independent DATA-header comparison, a consolidated
design/limitations reference, and an updated central evidence log.

Lucas's original manual ADS workflow and controlled evidence remain the basis
for validation and later recovery. The plan now explicitly describes the
documented manual procedure.

## Subtasks completed

| Owner | Work completed this week |
|---|---|
| Jeff | Revalidated record 41 data runs/slack and record 58 ADS metadata; independently checked resident DATA header values; documented design/limits; consolidated image evidence; documented the decision to retain manual ADS creation and adjusted the plan. |
| Lucas | Supplied the VM PowerShell listing of the eight files' full names and exact byte sizes, received October 18. |
| Jeff | Compared Lucas's exact-size evidence with the recorded parser logical sizes; all eight matched. Updated the manifest and validation records. |
| Lucas and Jeff | Met Tuesday, October 13 at 7:30 p.m. for planning. The Friday follow-up was moved to Saturday, October 17; reviewed remaining work/submission preparation and next week's tasks, with no issues reported. |

Lucas's earlier manual ADS steps remain the creation procedure; they are not
reported as a new Week 9 creation experiment.

## Detailed tests and demo evidence

### Test 1: Repeat real-image parser validation

**Input:** ADS/slack working RAW image.
**Method:** Inspect records 41 and 58 with `--show-record`.
**Expected:** Existing file metadata, data runs, slack range, and named ADS
agree with the manifests.
**Result:** Passed October 15. Record 41 showed Testfile.docx, logical size
13,437, allocation 16,384, LCN 3,659/four clusters, and 2,947 slack bytes at
16,049,277. Record 58 showed hostfile.txt, unnamed resident 31 bytes and
CapstoneEvidence resident 36 bytes. No image writes were made.
**Screenshots:** Captured October 15. The first shows the command, image
geometry, and record 41 identity/sizes. The second continues its data-run/slack
output and shows record 58's host name and both resident DATA streams.

![Week 9 parser command, boot geometry, and Testfile.docx in record 41.](evidence/week9/w9_parser_record41.png)

![Record 41 data run and slack range followed by hostfile.txt and the 36-byte CapstoneEvidence stream in record 58.](evidence/week9/w9_parser_slack_ads.png)

### Test 2: Independent resident DATA-header check

**Method:** PowerShell read record 58 at byte 3,222,333,440 without the Python
parser; walked bounded headers and decoded names and lengths directly.
**Expected:** Match the parser and earlier VM source evidence.
**Result:** Passed. Unnamed DATA at record-relative attribute offset 312 was
31 bytes; CapstoneEvidence at offset 368 was 36 bytes. This is metadata
validation, not payload extraction.
**Evidence:** Results in [validation notes](../docs/week9_validation.md),
compared with the historical [VM stream screenshot](evidence/week7/w7_ads_stream_lengths.png).

### Test 3: Active automated regression suite

**Method:** Run `python -m unittest discover -s tests -v`.
**Expected:** All 31 parser/embedding tests pass with no skips or failures.
**Result:** Passed October 15: all 31 tests, no skips or failures. Jeff's
terminal screenshot shows a completed run in 0.123 seconds and `OK`.

![Week 9 terminal capture showing all 31 automated tests passing.](evidence/week9/w9_automated_tests.png)

### Test 4: Independent exact-size comparison of eight known files

**Input:** Lucas's guest-VM PowerShell file listing, received October 18,
and the parser's previously recorded unnamed DATA logical sizes.
**Method:** Compare full filenames and exact byte lengths for all eight
entries, rather than relying on rounded Explorer KB sizes.
**Expected:** Every controlled file has the same name and logical size.
**Result:** Passed, eight of eight match. Sizes range from Test.txt at
83 bytes to WaterfallTest.png at 277,325 bytes. The full comparison is in the
[known-file manifest](../docs/week6_known_file_manifest.md#exact-size-comparison-completed-october-18).
This closes the Milestone 3 size follow-up; it is not a file-content hash test.

![Guest-VM full filenames and exact byte sizes supplied by Lucas.](evidence/week9/w9_vm_exact_file_sizes.png)

## Lessons learned

- An independent metadata read strengthens confidence beyond repeating the
  same parser's output; metadata checks do not establish payload recovery.
- A documented manual workflow can remain the controlled creation method
  when the plan explicitly records that choice and evidence requirements remain.
- Historical manifests and screenshots should remain distinguishable from
  new tests and newly acquired images.
- The VM file listing provides exact byte counts rather than rounded KB
  values. One PowerShell command supplies the entire set, allowing direct
  comparison with parser logical sizes. A matching size is not a content hash.

## Contributions

Jeff completed the validation and documentation listed above.
Lucas supplied the independent VM exact-size evidence, and Jeff completed
the comparison. Both members participated in Tuesday planning and Saturday
review, where no issues were raised. Their completed journals record the
week's work and lessons:
[Jeff](../weekly_journals/2026-10-18_jeff_perez.md) and
[Lucas](../weekly_journals/2026-10-18_lucas_curtis.md).

## Progress compared with the plan

Milestone 5 was reached with the October 11 midterm submission. The original
schedule treated October 12 as the beginning of midterm preparation, but it
was the due date. This left less planned work for October 12 - 18, so the team
adjusted the week to focus on follow-up validation, documentation, and next
week's tasks.
The parser's ADS host/stream identification was rechecked, a `$DATA` result
was independently checked, and the design, limitations, and evidence records
were consolidated. These are this week's additional results supporting the
completed milestone.

The Milestone 3 exact-size validation follow-up was completed October 18:
all eight files match the independent VM listing. The plan explicitly specifies
the documented manual ADS creation procedure. Milestone 6 extraction and
recovered-payload hash validation remain future work.

The review meeting was rescheduled from Friday to Saturday, October 17 and
has been completed. The team discussed remaining submission work and next
week's planned recovery tasks; no issues were reported. The exact-size listing
was pending at that meeting and was subsequently received and compared October 18.

## Before submission

- Review and commit attributable contributions; push and review/merge the PR.
- Lucas submits the approved website URL by Sunday, October 18, 11:59 p.m.
