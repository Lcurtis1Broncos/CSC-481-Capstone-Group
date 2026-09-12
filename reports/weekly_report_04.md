# Week 4 Team Progress Report

**Reporting period:** September 7 - September 13, 2026  
**Team:** Lucas Curtis and Jeff Perez  

## Milestones achieved

### Read and validate the first MFT record

Jeff extended the read-only NTFS disk-image reader to locate, read, and validate MFT record 0 (`$Mft`). The program uses the boot-sector values to calculate the MFT byte offset:

```text
MFT start LCN × bytes per cluster
2005 × 1024 = 2,053,120
```

It reads the 1,024-byte MFT record at that offset and checks its `FILE` signature. The program also reports the first attribute offset, whether the record is in use, and whether it is a directory.

### Baseline image and evidence record

Lucas created a dedicated VirtualBox baseline disk for the project and
documented its configuration and initial evidence details. He also created a
full raw disk image for team testing and recorded its SHA-256 hash. The team
verified that the downloaded raw image matches the recorded hash. The image's
partition and NTFS-volume layout will be validated during the next parser test
cycle.

## Subtasks completed

| Team member | Subtask | Brief description |
|---|---|---|
| Jeff Perez | MFT record reader | Extended the NTFS reader to calculate the MFT location from the boot sector and read record 0 (`$Mft`) without modifying the image. |
| Jeff Perez | MFT header validation | Added parsing for the `FILE` record signature, first attribute offset, in-use flag, and directory flag. |
| Jeff Perez | Automated tests | Added three MFT-reader tests; the full test suite now has six passing tests. |
| Lucas Curtis | Baseline disk and image | Created a dedicated VirtualBox baseline disk and exported a full raw image for controlled testing. |
| Lucas Curtis | Evidence record | Documented baseline configuration details and recorded the image's SHA-256 hash. |

## Test results and demo evidence

### Test 1: Read the first MFT record from the controlled image

**Input:** `7-ntfs-undel.dd` controlled NTFS disk image  
**Expected:** The program should use the NTFS boot-sector values to find MFT record 0, read a complete 1,024-byte record, and validate its `FILE` header.  
**Result:** Passed.

The program reported:

```text
MFT start LCN:        2005
Bytes per cluster:    1024

First MFT record summary
  Record number:        0 ($Mft)
  Byte offset:          2053120
  Record size:          1024 bytes
  Record signature:     FILE
  FILE signature valid: True
  First attribute:      byte 56
  Record in use:        True
  Is directory:         False
```

**Demo screenshot — successful MFT record read**

![VS Code terminal showing the NTFS boot-sector summary and a successful read of MFT record 0 (`$Mft`).](evidence/week4/w4_mft_record_read.png)

### Test 2: Automated parser tests

**Expected:** The program should calculate the MFT offset correctly, read and parse a valid MFT record, identify an invalid `FILE` signature, handle valid cluster sizes, and reject an image shorter than one sector.  
**Result:** Passed — 6 of 6 tests passed.

```text
test_calculates_first_mft_record_offset ... ok
test_identifies_an_invalid_mft_signature ... ok
test_parses_1024_byte_clusters ... ok
test_parses_4096_byte_clusters ... ok
test_reads_and_parses_a_valid_mft_record ... ok
test_rejects_an_image_shorter_than_one_sector ... ok

Ran 6 tests
OK
```

**Demo screenshot — automated test results**

![VS Code terminal showing all six automated NTFS-reader tests passing.](evidence/week4/w4_automated_tests.png)

### Evidence item: Baseline image integrity

Lucas recorded the raw baseline-image hash. Jeff downloaded the image and
independently calculated the same SHA-256 value:

```text
3815401D2D948B474D1EC104E2C5277ADD1D8DBFAAC4861388319A37EF235814
```

**Result:** Passed. The matching hash confirms that the team's downloaded copy
matches the shared raw image.

Baseline disk configuration and acquisition details are recorded in the
project's baseline documentation.

## Lessons learned

- The MFT is NTFS's central record system for files, folders, and NTFS metadata files.
- The boot sector provides the MFT start LCN and cluster size needed to calculate an exact byte offset.
- `FILE` identifies an MFT record header; it is not the signature at the beginning of every ordinary file's contents.
- MFT record 0 (`$Mft`) is an active NTFS metadata record, and its attributes begin after the record header.
- A controlled VirtualBox disk and a recorded SHA-256 hash provide a safer,
  repeatable basis for later forensic testing.
- A file extension alone does not establish an image format; the image layout
  must be validated before parser results are treated as evidence.

## Contribution of each team member

| Team member | Contribution this week |
|---|---|
| Jeff Perez | Implemented and tested the first-MFT-record reader; ran it against the controlled NTFS image; captured program and test-result screenshots; completed a Week 4 individual journal. |
| Lucas Curtis | Created the dedicated VirtualBox baseline disk; documented its configuration and evidence details; created and shared the raw image; recorded its SHA-256 hash; completed the Week 4 journal; and merged completed team work into `main`. |

## Progress compared with the project plan

The team progressed from reading the NTFS boot sector to reading and validating
the first MFT record. This follows the planned incremental approach: use the
boot sector to locate the MFT, then build toward parsing MFT attributes.

The dedicated baseline disk and a hash-verified raw image are available. The
raw image is a full-disk image rather than a volume-only image, so the next
parser increment will identify the target partition before reading its NTFS
boot sector. This is a planned adjustment that supports more realistic
full-disk forensic analysis.

## Plan for Week 5

- Read the full-disk partition table and identify the baseline partition.
- Update the parser to read an NTFS boot sector at a partition offset.
- Validate boot-sector output against the hash-verified baseline image.
- Prepare a known-file validation set and parser-review notes.
