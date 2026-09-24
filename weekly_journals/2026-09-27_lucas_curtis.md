# Weekly Journal - Lucas Curtis

**Week:** 6  
**Reporting period:** September 21 - September 27, 2026  
**Status:** Draft through September 24; review and finalize after the Friday summary meeting.

## Work completed

- Created the eight-file validation set in the dedicated unencrypted
  `NTFS_BASELINE (D:)` VirtualBox volume. The set includes text, Word, PDF,
  JPEG, PNG, HTML, and JSON files.
- Captured a VirtualBox File Explorer screenshot showing the known files in the
  controlled NTFS volume.
- Exported the updated full-disk RAW image containing the validation set and
  recorded its SHA-256 hash:
  `053D7CF98D07AAAEE265A1B4D027B384C528ABC55F1D59310B9BFDEE2CB76691`.
- Created the Week 6 meeting-minutes file and scheduled the team's planning
  and summary discussion.
- Provided the image and evidence needed for Jeff to validate the MFT
  file-listing feature against the known files.

## What I learned

A known-file set gives the team a controlled way to validate forensic-parser
output. The files must exist in the virtual-machine NTFS volume before the RAW
image is exported; placing similarly named files only in the GitHub repository
would not validate the MFT records in the image. A recorded image hash helps
identify the exact exported image used for the test.

## Problems encountered and resolution

The team originally planned a ten-file validation set. The controlled VM
evidence confirmed eight visible test files, so the team updated the Week 6
Milestone 3 measurement to use the eight-file set actually created and
validated. Two additional `$...txt` entries found by the parser were excluded
because they were not part of the controlled visible set.

## Plan for next week

- Review the Week 6 manifest, report, and evidence during the Friday summary
  meeting.
- Begin preparing the controlled ADS workflow for Milestone 4.
- Continue recording hashes, screenshots, and test details as the project
  image changes.
