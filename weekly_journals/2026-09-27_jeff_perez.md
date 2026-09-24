# Weekly Journal - Jeff Perez

**Week:** 6  
**Reporting period:** September 21 - September 27, 2026  
**Status:** Draft through September 24; update after the summary meeting.

## Work completed

- Reviewed the structure of an NTFS MFT record and learned how the record
  header identifies the byte offset of the first attribute.
- Extended the read-only Python reader to walk through the attributes in an
  in-use MFT record by using each attribute's type and length.
- Added support for decoding resident `$FILE_NAME` attributes from UTF-16LE
  bytes into readable file names.
- Added an optional `--list-files RECORDS` command-line setting that scans a
  selected number of MFT records and prints decoded file names.
- Added automated tests for `$FILE_NAME` decoding and file-name listing. The
  test suite now has 12 passing tests.
- Ran the reader against the full 8 GiB NTFS image containing Lucas's added
  files. The reader found the eight visible validation files in MFT records
  38, 39, 41, 42, 43, 44, 55, and 56.
- Updated the Milestone 3 success criterion in the semester plan from ten
  files to the team's confirmed eight-file validation set.

## What I learned

An MFT record is made of variable-length attributes rather than one fixed
layout for every file. A parser begins at the first-attribute offset in the
record header, reads an attribute's type and length, and moves forward by that
length until it finds `$FILE_NAME` or the end marker. `$FILE_NAME` stores the
name as UTF-16LE text, which must be decoded before it can be displayed.

I also learned that a successful forensic test needs both sides of the
comparison: evidence that the files were created in the controlled NTFS volume
and independent parser output showing the same names from the exported image.

## Problems encountered and resolution

The parser listed two additional `$...txt` names that do not appear in the
virtual-machine screenshot. Because Lucas did not identify them as part of the
known-file set, I excluded them from the eight-file validation comparison.
The team updated the Week 6 measurement in the project plan to match the eight
confirmed visible files.

## Plan for next week

- Parse additional metadata from `$STANDARD_INFORMATION`, `$FILE_NAME`, and
  `$DATA` attributes.
- Begin the controlled Alternate Data Stream (ADS) workflow described in
  Milestone 4.
- Add Week 6 screenshots and final test details to the team report after the
  summary meeting.
