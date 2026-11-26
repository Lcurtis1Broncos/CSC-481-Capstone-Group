# NTFS Filesystem Steganography and Forensic MFT Parser

## Project Summary

**CSC-481 Capstone, Team 3 — Lucas Curtis and Jeff Perez**

**Completed materials: November 26, 2026**

The project demonstrates controlled data hiding in NTFS alternate data
streams (ADS) and final-cluster file slack, followed by read-only recovery
from a raw disk image. A dedicated Windows VirtualBox laboratory provides
the evidence image. Python tools interpret filesystem metadata, locate
documented content, export recovered bytes, and save verification reports.

## Implementation

The parser reads partition and NTFS boot information, locates MFT records,
and interprets `$STANDARD_INFORMATION`, `$FILE_NAME`, and `$DATA` attributes.
The recovery path validates record fixups, distinguishes resident content
from nonresident data runs, selects named streams, and calculates bounded
final-cluster slack ranges. It refuses existing output destinations and
unsupported or invalid structures. The separate slack embedding tool writes
only a new controlled image copy; ADS creation uses the documented manual
PowerShell workflow.

## Results

- Recovered the 36-byte `CapstoneEvidence` ADS marker with its expected SHA-256.
- Recovered the 25-byte slack marker from image byte 16,049,277 with its expected
  SHA-256. The host's calculated slack capacity is 2,947 bytes.
- Matched all eight baseline-file lengths. Jeff confirmed original/recovered
  SHA-256 matches for all eight files on November 25; the dated confirmation
  preserves that provenance separately from the earlier machine logs.
- Passed 68 release tests and seven clean-copy acceptance checks on November
  24. The report branch subsequently passed 73 tests on November 25.
- Recovered all 50 unchanged synthetic slack payloads exactly; the direct-read
  baseline also matched all 50. All 50 deliberately changed-bit cases failed
  their original-payload hash comparisons as intended.
- Completed a separate 100-image detection experiment. Named-stream screening
  measured 100% detection, 40% false positives, and 0% evasion. Literal slack
  marker search measured 60% detection, 0% false positives, and 40% evasion.
  Legitimate ADS controls explain the first rule's false positives; transformed
  markers explain the second rule's misses. These rates describe the constructed
  known-record cases, not general Windows-volume performance.
- Verified source preservation during the recorded recovery and detection checks.

## Contributions and Lessons

Lucas prepared the VirtualBox laboratory and image exports, supplied known-file
information, documented manual ADS creation and recovery workflows, organized
evidence, and contributed report drafts, slides, and integration work. Jeff
implemented the parser, slack-copy and recovery tools, verification reporting,
tests and dataset generation, recorded validation results, and assembled the
expanded report and reproducible evaluation campaigns. The report's contribution
appendix and repository history provide the supporting record.

The main lessons are that resident and nonresident content need different
recovery paths, data-run order matters, allocated bytes differ from logical
content, and hashes must be compared with trustworthy original expectations.
A named stream warrants inspection but does not establish concealment intent;
a fixed signature can miss transformed content.

## Scope and Final Delivery

The implementation supports the documented controlled-image paths. Fragmented
MFT storage, attribute-list resolution, encrypted/compressed recovery, and general
unknown-payload discovery remain outside scope. Synthetic fixtures are small
NTFS-shaped inputs, not independently acquired or mountable Windows volumes.
Large laboratory images remain outside Git; included generation scripts allow
the supported workflow to run without downloading those images.

The original midterm interval was adjusted after submission on October 11;
October 12–18 was used for validation and planning. Later work completed recovery,
ADS and slack validation, consolidated testing, and final packaging. The final
report is signed and dated, the slides and demo guide are prepared, and the code
release remains `v1.0-final`. The final speaking rehearsal, live presentation,
and course-site submissions require the presenters' completion and confirmation.

## Deliverables

- [Signed and dated final report](NTFS_Filesystem_Steganography_and_Forensic_MFT_Parser_final_report.pdf)
- [Presentation](../presentation/CSC481_NTFS_Capstone_Final_Presentation.pptx)
- [Demonstration guide](../presentation/DEMO_GUIDE.md)
- [Semester completion checklist](SEMESTER_COMPLETION_CHECKLIST.md)
- [Code release verification](COMPLETE_CODE_CHECKLIST.md)
- [Detection results](evidence/final_detection/README.md)
- [Eight-file hash confirmation](../docs/baseline_hash_verification.md)
