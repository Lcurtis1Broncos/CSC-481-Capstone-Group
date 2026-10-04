# Weekly Journal - Lucas Curtis

**Week:** 7  
**Reporting period:** September 28 - October 4, 2026  
**Status:** Complete  
**Preparation note:** Prepared by Jeff using Lucas's supplied evidence and
the work, learning, and problem details confirmed by Jeff after the team review.

## Work completed

- Created a controlled Alternate Data Stream manually using PowerShell on
  the dedicated NTFS volume in VirtualBox.
- Used `D:\ADS_Test\hostfile.txt` as the host file and `CapstoneEvidence` as
  the stream name.
- Recorded the payload marker, 36-byte length, and SHA-256 hash, and supplied
  screenshots showing the host file and its normal and named streams.
- Exported `NTFS_Forensic_Baseline_ADS_Created_RAW.dd`, calculated its SHA-256
  hash, and shared the image and supporting evidence with Jeff.
- Reviewed both members' work at the October 3 meeting at 7:30 p.m. The team
  confirmed that the parser functions and recognizes the controlled ADS.

The workflow was performed manually; a reusable script was not created this
week. Image integrity and parser results are documented in the
[ADS payload manifest](../docs/week7_ads_payload_manifest.md).

## What I learned

Lucas learned how to create an Alternate Data Stream attached to an NTFS
host file. He read supporting material and watched tutorials to learn how to
perform the steps correctly. He also documented the stream's byte length and
hash so the team can compare later parser and recovery results with the
controlled source evidence.

## Problems encountered

No problems were reported. Reading and tutorials helped Lucas prepare the
manual workflow before completing the experiment.

## Plan for next week

- Document the ADS creation workflow and working-image state, as assigned in
  the semester plan for October 5 - October 11.
- Retain the payload manifest, source screenshots, and image hash for later
  recovery validation.
- Attend the Monday, October 5 planning meeting at 7:30 p.m. to review the
  next week's work with Jeff.
