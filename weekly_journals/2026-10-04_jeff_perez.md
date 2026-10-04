# Weekly Journal - Jeff Perez

**Week:** 7  
**Reporting period:** September 28 - October 4, 2026  
**Status:** Complete

## Work completed

- Extended the read-only MFT parser to interpret `$STANDARD_INFORMATION`
  (`0x10`), `$FILE_NAME` (`0x30`), and `$DATA` (`0x80`) attributes.
- Added readable UTC timestamp and file-attribute-flag output from
  `$STANDARD_INFORMATION`.
- Added `$DATA` output for stream name, logical size, allocated size, and
  resident/nonresident state.
- Added `--show-record RECORD_NUMBER`, which allows a selected MFT record to
  be summarized without scanning the complete file list.
- Tested the feature against the controlled eight-file RAW image. The parser
  distinguished resident text/HTML/JSON files from nonresident Office, PDF,
  JPG, and PNG files.
- Confirmed that the parser recognizes existing named `Zone.Identifier`
  streams on two files. These are Windows metadata, not the team's controlled
  ADS payload.
- Added automated coverage for standard-information timestamps and flags,
  named resident and nonresident `$DATA`, MFT record offsets, and zero
  FILETIME values. The suite has 17 passing tests.
- Added yellow terminal highlighting for discovered file names to make parser
  output easier to review; the display change does not alter forensic data.
- Wrote the controlled slack-space embedding procedure draft and documented
  the parser's current metadata-only limitation.

## What I learned

The three attributes answer different questions. `$STANDARD_INFORMATION`
describes a file's timestamps and flags, `$FILE_NAME` identifies the file and
stores filename-related size information, and `$DATA` describes the actual
data stream. A `$DATA` attribute with a blank stream name is the normal file
contents; a nonblank stream name identifies an Alternate Data Stream.

I also learned that resident data is stored inside the MFT record, while
nonresident data is stored in clusters elsewhere in the volume. The parser
can describe both states now, but a later recovery feature must interpret
nonresident data runs before it can read file contents.

## Controlled ADS validation

On October 3, I independently verified the supplied ADS image SHA-256 against
Lucas's screenshot. The parser found `hostfile.txt` in record 58 and reported
the resident `CapstoneEvidence` stream at 36 bytes, matching his source
evidence. Its normal unnamed contents are 31 bytes. I documented the actual
stream name, marker, lengths, and source hashes in the ADS payload manifest.
Payload recovery and an independent recovered-payload hash check remain
future work.

## Plan for next week

- Extend the controlled ADS validation toward content recovery as scheduled.
- Begin documented slack-space test setup after team review of the lab-only
  procedure.
- Extend the parser toward named-stream and nonresident-data-run handling.
