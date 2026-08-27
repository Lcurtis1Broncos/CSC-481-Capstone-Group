# Project Plan: NTFS Filesystem Steganography and Forensic MFT Parser

## 1. Project Purpose

Build a controlled NTFS forensic laboratory that demonstrates two data-hiding techniques—Alternate Data Streams (ADS) and cluster slack space—and a read-only forensic recovery tool that reconstructs those artifacts directly from an NTFS `.dd` disk image.

All experiments will use a dedicated VirtualBox disk image. No tool will write to a physical drive.

## 2. Objectives

1. Create a small NTFS volume in a VirtualBox virtual disk.
2. Develop a Python raw-sector parser that:
   - Reads the NTFS boot sector.
   - Calculates sector, cluster, and MFT geometry.
   - Parses MFT record headers and attribute lists.
   - Extracts `$STANDARD_INFORMATION`, `$FILE_NAME`, and `$DATA` attributes.
   - Identifies named `$DATA` attributes, including ADS.
3. Develop an image-generation/hiding tool that embeds controlled test payloads in:
   - An Alternate Data Stream.
   - Slack space within the final allocated cluster of a small host file.
4. Develop a read-only forensic extractor that scans the MFT and recovers:
   - File metadata.
   - Resident and non-resident file data where supported.
   - ADS names and contents.
   - Slack-space payloads based on documented test markers.
5. Produce a reproducible `.dd` image, technical report, hex-dump evidence, and live demonstration.

## 3. Scope and Safety Boundaries

In scope:

- Offline NTFS `.dd` images created specifically for this project.
- Direct binary reads of images and controlled writes to a copied lab image.
- ADS detection and recovery from MFT `$DATA` attributes.
- Slack-space examination of known test files.
- Documentation of limitations and evidence integrity.

Out of scope:

- Physical disks, removable drives, production systems, or third-party images without authorization.
- Encryption bypass, credential recovery, persistence mechanisms, or live-system anti-forensics.
- General-purpose destructive disk-writing tools.

## 4. Team Roles

| Role | Primary responsibilities | Key outputs |
|---|---|---|
| Team Leader | NTFS specification research, integration, repository standards, report structure, validation plan, demo coordination | Architecture, milestone reviews, final report and demo |
| Member A | Raw NTFS parser: boot sector, MFT location, record parsing, attribute parsing, runlists, metadata display | `ntfs_parser` module and MFT listing tool |
| Member B | Controlled hiding workflow, ADS and slack embedding, recovery logic, test payload catalog | Image builder, hiding tool, extractor modules |

All members should review binary parsing code and independently verify at least one test image.

## 5. Technical Architecture

```text
VirtualBox NTFS disk
        |
        v
Forensic copy / exported .dd image
        |
        +--> Python NTFS parser (read-only)
        |      Boot sector -> MFT -> attributes -> files/ADS
        |
        +--> Slack analyzer
        |      File size + allocated clusters -> trailing slack bytes
        |
        +--> Evidence outputs
               JSON/CSV inventory, extracted payloads, hexdumps, hashes
```

Recommended repository structure:

```text
project/
  docs/
    ntfs-notes.md
    test-plan.md
    evidence-log.md
  images/
    baseline.dd
    hidden-data.dd
  tools/
    create_lab_image.py
    hide_ads.py
    embed_slack.py
    parse_ntfs.py
    extract_hidden.py
  ntfs/
    boot_sector.py
    mft.py
    attributes.py
    runlist.py
    slack.py
  tests/
    fixtures/
    test_boot_sector.py
    test_mft.py
    test_runlist.py
    test_extraction.py
  output/
    mft_inventory.json
    ads_report.json
    slack_report.json
    recovered/
```

## 6. Core Implementation Plan

### A. NTFS Image Preparation

- Create a small dedicated NTFS virtual disk, preferably 1–4 GB.
- Record partition layout, NTFS version, bytes per sector, sectors per cluster, and volume serial number.
- Export a clean baseline image before embedding test data.
- Create a copied working image for every write experiment.
- Hash baseline and working images using SHA-256 before and after each controlled action.

### B. Boot Sector Parser

Parse the NTFS volume boot record at the start of the NTFS partition.

Required fields:

- OEM ID (`NTFS    `)
- Bytes per sector
- Sectors per cluster
- Cluster size
- MFT logical cluster number
- MFT mirror logical cluster number
- MFT record size
- Index record size
- Volume serial number

Validation:

- Confirm boot-sector values against a trusted NTFS inspection utility.
- Verify the computed MFT byte offset:
  `MFT offset = MFT LCN × cluster size`.

### C. MFT Record Parser

Implement parsing for 1024-byte MFT records, while honoring the record size specified by the boot sector.

Required parsing stages:

1. Confirm `FILE` record signature.
2. Apply Update Sequence Array fixups before parsing attributes.
3. Read record flags and identify allocated versus deleted records.
4. Locate the first attribute offset.
5. Walk attributes until the end marker (`0xFFFFFFFF`).
6. Support both resident and non-resident attributes.
7. Decode UTF-16LE names.

Initial attribute support:

- `$STANDARD_INFORMATION` (`0x10`)
- `$FILE_NAME` (`0x30`)
- `$DATA` (`0x80`)
- `$ATTRIBUTE_LIST` (`0x20`) as a documented future extension if not completed
- `$BITMAP` and `$INDEX_ROOT` as optional enhancements

Output fields:

- MFT record number
- In-use/deleted state
- File flags
- Parent record reference
- Filename/path where reconstructable
- Logical size and allocated size
- Data attribute name
- Resident/non-resident state
- Data runs and disk offsets for non-resident data

### D. ADS Hiding and Recovery

Controlled payload design:

- Use a short plaintext marker such as `ADS_PROJECT9::<case-id>::<message>`.
- Attach it as a named stream to a harmless test file.
- Keep a manifest that records host filename, stream name, payload size, SHA-256, and expected MFT record.

Recovery requirements:

- Identify every named `$DATA` attribute.
- Distinguish the unnamed/default data stream from ADS.
- Recover resident ADS data directly from the MFT record.
- Recover non-resident ADS data by decoding data runs and reading clusters from the image.
- Produce a report containing stream name, host file, size, hash, and recovered output path.

### E. Slack-Space Embedding and Recovery

Controlled embedding design:

- Use a small host file whose logical size is much smaller than one cluster.
- Identify its allocated cluster(s) through its non-resident `$DATA` runlist.
- Preserve the logical file bytes.
- Write only after the logical end-of-file offset and only within the allocated final cluster.
- Embed a recognizable structure, for example:

```text
P9SLACK|version=1|length=<n>|sha256=<hash>|<payload>
```

Recovery requirements:

- Locate the host file via MFT parsing.
- Calculate:
  - Logical size.
  - Allocated size.
  - Final cluster.
  - Slack range from EOF to the end of the final allocated cluster.
- Read the slack range directly from the image.
- Search for the test marker.
- Validate recovered payload length and SHA-256 hash.
- Clearly distinguish recoverable test data from unrelated residual slack bytes.

## 7. Milestone Schedule

| Week | Activities | Acceptance criteria |
|---|---|---|
| W2 | Confirm scope, create repository, assign roles, begin NTFS specification study | Semester plan, risk register, initial architecture |
| W3 | Build VirtualBox NTFS lab volume and collect baseline metadata | Baseline image and hash manifest |
| W4 | Export first `.dd` image; validate image offsets and boot sector manually | Boot-sector field worksheet agrees with parser calculations |
| W5 | Implement boot-sector and basic MFT record parsing | Tool lists valid MFT records and filenames |
| W6 | Parse `$STANDARD_INFORMATION`, `$FILE_NAME`, and resident `$DATA` | Metadata inventory exported as JSON/CSV |
| W7 | Implement non-resident `$DATA` parsing and runlist decoding | Parser recovers at least three ordinary files correctly |
| W8 | Create ADS and slack test cases; prepare midterm report | Both hiding methods demonstrated in controlled image |
| W9 | Add ADS enumeration and resident ADS extraction | ADS stream detected and recovered from image |
| W10 | Add non-resident ADS extraction and slack-range calculation | Extractor identifies expected disk offsets |
| W11 | Complete automated forensic extraction workflow | Single command produces inventory and recovered artifacts |
| W12 | Test normal, fragmented, empty, deleted, and malformed-record cases | Test report with expected vs. actual results |
| W13 | Produce hex-dump evidence and validate hashes | Evidence log links offsets, hex dumps, and hashes |
| W14 | Draft final report and create demonstration dataset | Complete reproducible instructions |
| W15 | Rehearse live demo; finalize slides and report | Dry run succeeds from clean checkout |
| W16 | Final presentation and submission | Deliverables packaged and verified |

## 8. Test Campaign

### Functional Tests

- Parse a valid NTFS boot sector.
- Reject invalid signatures and unsupported geometry safely.
- Parse at least 50 MFT records.
- Identify normal files, directories, deleted records, and named `$DATA` streams.
- Recover a resident ADS.
- Recover a non-resident ADS.
- Recover the known slack payload.
- Handle a fragmented file using multiple data runs.
- Confirm that ordinary visible file contents remain unchanged after slack embedding.

### Integrity Tests

- Compare each recovered payload hash to its known source hash.
- Record source image SHA-256 before parsing.
- Verify the recovery tool never modifies the image.
- Verify the hiding tool only modifies an explicitly selected working image.
- Preserve baseline, pre-hide, and post-hide images separately.

### Negative Tests

- Image with no ADS.
- Image with no recognized slack marker.
- Corrupt MFT signature.
- Invalid update-sequence fixup.
- Invalid runlist.
- Truncated image.
- ADS with Unicode stream name.
- Host file with no available slack.

## 9. Evidence and Documentation Requirements

For each hidden artifact, document:

- Image filename and SHA-256
- Case identifier
- Host file path and MFT record number
- ADS name or slack range
- Cluster number(s) and absolute byte offsets
- Payload length and SHA-256
- Hex dump showing the marker and payload region
- Extraction command and output hash
- Screenshot or terminal capture of successful recovery

Maintain a chain-of-custody-style evidence log, even though this is a lab project. This makes the final report more credible and ensures every result is reproducible.

## 10. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Corrupting the lab image | Never modify the baseline; create a new copied image for every embedding attempt |
| Incorrect MFT parsing due to fixups | Implement and test Update Sequence Array handling before attribute parsing |
| Fragmented files complicate recovery | Start with contiguous test files, then add fragmentation as a planned test case |
| ADS not visible through normal file listing | Treat named `$DATA` attributes as the forensic source of truth |
| Slack contents overwritten by filesystem activity | Perform slack writes only after the image is finalized; avoid subsequent guest OS activity |
| Unclear evidence offsets | Generate machine-readable reports and retain hexdumps with byte offsets |
| Unsupported NTFS structures | Explicitly document supported attributes and fail safely on unsupported cases |

## 11. Final Deliverables

1. `hide_ads.py` or equivalent controlled ADS embedding workflow.
2. `embed_slack.py` that performs direct writes only to a specified copied lab image.
3. `extract_hidden.py`, a read-only NTFS image parser and recovery tool.
4. Python modules for boot-sector, MFT, attribute, runlist, ADS, and slack parsing.
5. A reproducible `.dd` image containing documented test artifacts.
6. Baseline and final image SHA-256 manifest.
7. JSON/CSV MFT inventory and hidden-data recovery report.
8. Hex-dump evidence package.
9. Test plan and completed test results.
10. Final report, presentation slides, and live demo script.

## 12. Definition of Done

The project is complete when a reviewer can take the supplied `.dd` image, run the read-only parser, and independently verify:

- The NTFS geometry and MFT location are correctly derived from raw disk structures.
- The MFT inventory identifies the host files and named `$DATA` streams.
- The ADS payload is recovered without OS-level filesystem APIs.
- The slack payload is recovered from the documented EOF-to-cluster-end range.
- Recovered payload hashes match the original controlled test payloads.
- The report provides sufficient offsets, hashes, and hex evidence to reproduce each finding.