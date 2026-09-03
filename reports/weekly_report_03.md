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

### [Lucas: Add your Week 3 milestone(s)]

Describe the controlled test environment, image preparation, project planning,
research, or other work completed during this week.

## Subtasks completed

| Team member | Subtask | Brief description |
|---|---|---|
| Jeff Perez | NTFS fundamentals research | Studied disk sectors and clusters, MFT records, ADS, file slack, `.dd` images, and the NTFS boot sector. |
| Jeff Perez | Boot-sector reader | Implemented the first Python reader for NTFS disk images. |
| Jeff Perez | Reader testing | Added automated tests and tested the reader against a controlled NTFS image. |
| Lucas Curtis | **[Lucas: add subtask]** | **[Lucas: add a brief description]** |

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
- **[Lucas: Add screenshot(s) and captions for your completed subtask tests.]**

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
- **[Lucas: Add lessons learned from your work.]**

## Contribution of each team member

| Team member | Contribution this week |
|---|---|
| Jeff Perez | Completed NTFS research and lessons; implemented and tested the initial boot-sector reader; created the Week 3 individual journal; opened pull request #7 for the code contribution. |
| Lucas Curtis | **[Lucas: describe your Week 3 contribution, commit(s), testing, and documentation.]** |

## Progress compared with the project plan

Jeff's Week 3 objective—understanding NTFS basics and producing an initial
raw disk-image/boot-sector reader—was achieved. The code is ready for review
and provides a foundation for locating and reading MFT records next week.

**[Lucas: State whether the team is on schedule overall. If not, describe the
adjustment to the plan and timeline.]**

## Plan for Week 4

- Use the boot-sector values to locate and read the first MFT record.
- Begin identifying MFT record headers and basic attributes such as
  `$STANDARD_INFORMATION`, `$FILE_NAME`, and `$DATA`.
- Continue controlled-image testing and document all expected and actual
  results.
- **[Lucas: Add the team’s agreed Week 4 task(s).]**
