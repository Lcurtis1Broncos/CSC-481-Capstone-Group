# Weekly Journal - Jeff Perez

**Week:** 8  
**Reporting period:** October 5 - October 11, 2026  
**Status:** Complete

## Work completed

- Attended the Monday, October 5 planning meeting at 7:30 p.m. with Lucas
  and reviewed our assignments for the week.
- Extended the NTFS parser to decode nonresident `$DATA` runs and report each
  run's starting cluster, cluster count, and absolute byte offset in the image.
- Added support for signed cluster-location changes between runs and
  recognition of sparse runs, with checks for malformed data-run bytes.
- Added final-cluster slack calculations using the file's logical size and
  decoded data runs. The calculation follows the final file cluster even when
  a file is fragmented and excludes extra preallocated clusters.
- Implemented `code/slack_embed.py` for the controlled lab experiment. It
  creates a new image copy, verifies the known source hash, and writes the
  marker only within the selected file's slack range.
- Used `Testfile.docx` in MFT record 41 as the controlled host. Its contents
  occupy 13,437 bytes in 16,384 bytes of allocated space, leaving 2,947 bytes
  in the final cluster. The calculated slack begins at image byte 16,049,277.
- Embedded the 25-byte UTF-8 marker `TEAM3_SLACK_TEST_20261008` in
  `NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd`. The original ADS image was
  preserved. A full comparison verified that only the marker range changed.
- Generated a payload manifest containing the marker, length, exact location,
  source and working-image hashes, payload hash, and verification result.
- Read the marker back independently using PowerShell and confirmed its
  25-byte length and SHA-256 against the manifest:

```text
3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2
```

- Confirmed the parser still reports the original host-file metadata and the
  existing `CapstoneEvidence` ADS in record 58 of the working image.
- Expanded the automated suite to 31 passing tests, including fragmented
  runs, sparse runs, malformed inputs, slack boundaries, copy protection,
  marker-only modification, and MFT sector-tail fixups in the embedding tool.
- Captured screenshots of the parser's data-run/slack output, all 31 passing
  tests, and the PowerShell marker read-back with matching hash.
- Updated the controlled slack-space procedure with the implemented commands
  and validation steps.

## What I learned

A data run contains directions to a nonresident file's clusters. The starting
cluster and cluster count tell the parser where each part of the file is
stored. Multiplying a cluster number by the cluster size and adding the NTFS
partition offset gives its absolute byte position in a full-disk image.

Logical size is the amount of actual file content, while allocated size is the
cluster space reserved for it. The unused tail after the file ends in its final
cluster is slack. For fragmented files, the parser must follow the data runs
to the cluster containing the logical end rather than assume all allocated
space is consecutive.

I also learned how a known marker and recorded SHA-256 hash make a controlled
experiment verifiable. Reading the marker from the recorded offset and
matching its hash confirms that the expected bytes are present there.

## Problems encountered and resolution

The first automated-test screenshot cropped the final `OK` summary. I reduced
the VS Code zoom and captured a replacement showing the full test result.
No failing tests or real-image validation errors were observed in the
completed work.

## Limitations

The embedding tool is restricted to the verified ADS lab image and ordinary
nonresident streams with complete data runs. It does not embed into resident,
compressed, sparse, encrypted, or extension-record streams. The marker
read-back checks a known location; generalized payload discovery and recovery
remain later project work.

## Plan for next week

- Validate parser results and document limitations for the midterm package.
- Review the ADS and slack-space manifests, hashes, screenshots, and test
  results with Lucas.
- Support the midterm evidence and report preparation for October 12 - 18.

## Supporting evidence

- [Week 8 evidence and screenshots](../reports/evidence/week8/README.md)
- [Slack payload manifest](../reports/evidence/week8/w8_slack_payload_manifest.json)
- [Controlled slack-space procedure](../docs/controlled_slack_space_procedure.md)
- [Week 8 meeting minutes](../meeting_minutes/2026-10-05.md)
