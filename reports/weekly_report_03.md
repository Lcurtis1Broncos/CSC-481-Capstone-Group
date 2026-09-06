# Week 3 Team Progress Report

**Reporting period:** August 31 - September 6, 2026  
**Team:** Lucas Curtis (team leader) and Jeff Perez

> Before the team leader submits this report to Canvas, Lucas should complete
> every item marked **[Lucas: ...]** and add the required screenshots below.

## Milestones achieved

### Initial NTFS disk-image reader

Jeff completed the first working component of the NTFS forensic parser. The
reader opens a `.dd` disk image in read-only mode, reads the first 512 bytes,
and displays a hex/ASCII view of that data. It then extracts introductory NTFS
boot-sector information: the NTFS signature, bytes per sector, sectors per
cluster, cluster size, MFT start logical cluster number (LCN), MFT record size,
and the boot-sector signature.

The reader and its tests were submitted in pull request #7 for team-leader
review.

### Controlled practice image selected

The team selected the `7-ntfs-undel.dd` controlled NTFS practice image for
early testing. This supports safe, repeatable development without accessing a
personal computer's drive.

### NTFS research and evidence documentation

Lucas documented NTFS on-disk structures and their forensic value. He also
created a definitions page covering major NTFS fields, including the boot
sector, MFT, and data attributes. In addition, he created an evidence-log
template to help the team record collected evidence in a consistent format.

## Subtasks completed

| Team member | Subtask | Brief description |
|---|---|---|
| Jeff Perez | NTFS fundamentals research | Studied disk sectors and clusters, MFT records, ADS, file slack, `.dd` images, and the NTFS boot sector. |
| Jeff Perez | Boot-sector reader | Implemented the first Python reader for NTFS disk images. |
| Jeff Perez | Reader testing | Added automated tests and tested the reader against a controlled NTFS image. |
| Lucas Curtis | NTFS on-disk structure research | Documented important NTFS structures and why they matter during forensic analysis. |
| Lucas Curtis | NTFS definitions reference | Created a reference page for the boot sector, MFT, and data attributes. |
| Lucas Curtis | Evidence-log template | Created a reusable format for recording evidence details as the project develops. |

## Test results and demo evidence

### Test 1: Controlled NTFS `.dd` image

**Input:** `7-ntfs-undel.dd` (6,160,384 bytes)  
**Expected:** The program should identify a valid NTFS boot sector and report
its storage geometry and MFT location.  
**Result:** Passed.

The reader reported:

```text
OEM ID:               NTFS
NTFS signature valid: True
Bytes per sector:     512
Sectors per cluster:  2
Bytes per cluster:    1024
MFT start LCN:        2005
MFT record size:      1024 bytes
Boot signature valid: True
```

### Test 2: Automated parser tests

**Expected:** The parser should correctly handle different valid NTFS cluster
layouts and reject an input that is too short to contain one sector.  
**Result:** Passed — 3 of 3 tests passed.

```text
test_parses_1024_byte_clusters ... ok
test_parses_4096_byte_clusters ... ok
test_rejects_an_image_shorter_than_one_sector ... ok

Ran 3 tests
OK
```

### Test 3: Non-NTFS input warning

**Expected:** A normal file should not be incorrectly presented as a valid
NTFS boot sector.  
**Result:** Passed. The program displayed a warning that the selected input
did not appear to be an NTFS boot sector.

### Required screenshots before submission

- **[Add Screenshot 1]** Terminal output from Test 1 showing the valid NTFS
  signature, 1,024-byte cluster size, and MFT start LCN.
- **[Add Screenshot 2]** Terminal output from Test 2 showing all three
  automated tests passing.
- **[Add Screenshot 3]** GitHub view of Lucas's NTFS research and evidence-log
  template, with a short caption identifying the documents.

## Lessons learned

- NTFS allocates storage in whole clusters. Unused bytes in the final cluster
  allocated to a file are called file slack and may contain residual data.
- The MFT is the central NTFS record system that helps locate files and their
  attributes.
- ADS is a legitimate NTFS feature that may hold metadata, but it can also be
  relevant forensic evidence when evaluated with other context.
- The boot sector is the starting map for a parser because it supplies the
  cluster size and the MFT location.
- Small, tested components are a practical way to build a forensic parser.
- Lucas developed a better overall understanding of the important NTFS data
  structures the team will need to examine during the project.

## Contribution of each team member

| Team member | Contribution this week |
|---|---|
| Jeff Perez | Completed NTFS research and lessons; implemented and tested the initial boot-sector reader; created the Week 3 individual journal; opened pull request #7 for the code contribution. |
| Lucas Curtis | Added NTFS on-disk structure research, an NTFS definitions reference, and an evidence-log template; completed his Week 3 journal; reviewed and merged the boot-sector reader pull request. |

## Progress compared with the project plan

The team achieved its Week 3 research and initial-parser objectives. Jeff's
boot-sector reader has been merged into `main`, while Lucas completed the
supporting NTFS research and evidence documentation.

The dedicated VirtualBox NTFS disk and clean baseline `.dd` image were moved
to Week 4. The adjustment is to complete that controlled test environment
early in Week 4 and use it while the team begins reading MFT records.

## Plan for Week 4

- Use the boot-sector values to locate and read the first MFT record.
- Begin identifying MFT record headers and basic attributes such as
  `$STANDARD_INFORMATION`, `$FILE_NAME`, and `$DATA`.
- Continue controlled-image testing and document all expected and actual
  results.
- Lucas will create the dedicated VirtualBox NTFS disk, export a clean
  baseline `.dd` image, and record its evidence details.
