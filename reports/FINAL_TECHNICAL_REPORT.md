# Final Technical Report — Review Draft

**Project:** NTFS Filesystem Steganography and Forensic MFT Parser  
**Course:** CSC-481 Capstone  
**Team:** Team 3  
**Members:** Lucas Curtis and Jeff Perez  
**Prepared:** November 17, 2026  
**Status:** DRAFT (Jeff's Approval Pending)

## Abstract

This capstone investigates forensic identification and recovery of data concealed in two NTFS storage locations: named Alternate Data Streams (ADS) and unused bytes in the final allocated cluster of a file (file slack). The team developed Python tooling to interpret raw NTFS images, locate partitions and Master File Table (MFT) records, decode file attributes and data runs, and export selected file contents and controlled hidden payloads. Validation used a dedicated VirtualBox NTFS disk, recorded manifests, image SHA-256 hashes, Windows filesystem comparisons, and automated regression tests. In the November 15, 2026 validation, 64 automated tests passed; eight baseline files matched expected names and byte lengths; and both the 36-byte ADS marker and 25-byte slack marker were recovered with SHA-256 matches to their original manifests. The working image hash did not change during recovery.
## 1. Introduction

NTFS organizes file metadata in the Master File Table and stores content in resident attributes or disk clusters referenced by nonresident data runs. Two locations can hold information that may not be apparent in a conventional file listing: a named `$DATA` stream attached to a host file and the unused tail of a file's last allocated cluster. Both are relevant to digital forensics because a filename-only examination may overlook them.

**Problem statement:** Determine whether a purpose-built, read-only Python parser can identify NTFS metadata and recover controlled ADS and slack-space payloads from raw disk images while preserving source integrity.

**Objectives:** (1) acquire and document a readable unencrypted NTFS baseline; (2) parse partition and MFT structures; (3) validate known files; (4) create and document controlled ADS and slack payloads; (5) recover those payloads and compare lengths and SHA-256 hashes; and (6) run repeatable regression tests and record limitations.

## 2. Background

An NTFS volume's boot sector describes sector and cluster geometry, MFT location, and record size. Each MFT file record contains typed attributes, including `$STANDARD_INFORMATION` (metadata and timestamps), `$FILE_NAME` (filename metadata), and `$DATA` (file contents). Small data may be resident in the MFT record; larger data may be nonresident and mapped through data runs to logical cluster numbers (LCNs). Named `$DATA` attributes support ADS. File slack is the part of the last allocated cluster beyond the file's logical end; it is distinct from the file's logical content and may contain residual or deliberately placed bytes.

Forensic interpretation requires correct partition-relative offsets, update sequence array (USA) fixup handling, run decoding, and strict bounds checking. A calculated slack range is not proof of hidden data; payload identification and independent hash comparison provide stronger evidence.

## 3. Environment and evidence acquisition

The team used a dedicated Windows VirtualBox lab with an 8 GiB virtual disk and exported raw `.dd` images. The initial image contained a BitLocker header (`-FVE-FS-`) and was not suitable for direct NTFS parsing. The team recreated an unencrypted baseline and verified its image SHA-256. Later image states added eight known files, a named ADS, and a controlled slack marker. The slack marker was embedded into a separate working copy rather than the source image. Raw images and recovered binary files were kept outside GitHub; the repository contains source code, manifests, JSON validation records, text logs, screenshots, and reports.

The validated unencrypted image used MBR partition type `0x07`, start LBA 2,048, 512-byte sectors, 4,096-byte clusters, 1,024-byte MFT records, and MFT start LCN 786,432. The NTFS partition begins at byte 1,048,576 and the first MFT record at absolute image offset 3,222,274,048. Parser results were compared with Windows `fsutil fsinfo ntfsinfo D:` and agreed on the recorded fields.

The five image-state SHA-256 values, provenance, and qualifications are preserved in `FINAL_FORENSIC_EVIDENCE_LOG.md` and `docs/Baseline Evidence.md`.

## 4. System design and implementation

### 4.1 Read-only NTFS parser

The Python image reader parses the disk partition table, selects the NTFS partition, reads boot-sector geometry, computes absolute MFT offsets, and interprets selected records and attributes. Its documented capabilities include `$STANDARD_INFORMATION`, `$FILE_NAME`, and `$DATA` summaries, resident and nonresident stream identification, named-stream enumeration, and data-run decoding. Parser test cases exercise geometry, malformed records, fragmented runs, and unsupported layouts.

### 4.2 Recovery utility

The recovery component exports selected resident data from USA-restored MFT records and nonresident content from mapped data extents. For named streams, selection must match the requested stream name. Slack recovery calculates the final cluster's unused byte range and permits a bounded extraction rather than indiscriminately exporting the entire allocated cluster. Recovery writes to a separate output path; the source image remains read-only. Tests include refusals for malformed geometry, unsafe destinations, unsupported streams, out-of-range slack requests, and mismatched expected hashes.

### 4.3 Validation and reporting

Evidence manifests provide expected sizes, names, offsets, and hashes where available. Machine-readable JSON records preserve actual recovered sizes, hashes, source-image before/after hashes, and status. Test results distinguish **PASS**, **FAIL**, and **NOT VERIFIED**, so absence of an original content hash is not misreported as success.

## 5. Experimental methodology

1. **Preserve and characterize images:** Record the filename, acquisition state, SHA-256, partition start, NTFS geometry, and operator details.
2. **Validate filesystem metadata:** Compare parser-derived NTFS fields and MFT positions with Windows and manual sector inspection.
3. **Prepare known-file set:** Create eight controlled files of different formats; record names, MFT records, and exact guest-VM byte lengths.
4. **Create ADS marker:** Place a known 36-byte ASCII marker in `hostfile.txt:CapstoneEvidence`; document its original SHA-256.
5. **Create slack marker:** Determine `Testfile.docx`'s final-cluster slack, place a 25-byte marker into a working-image copy, and record the expected hash.
6. **Recover data:** Use the parser and recovery utility to export file contents, the named ADS, and the selected slack bytes.
7. **Validate and report:** Compare recovered lengths and, where original values exist, recovered SHA-256 values. Confirm source-image integrity before and after extraction and run the automated regression suite.

## 6. Results

### 6.1 NTFS and MFT parsing

The parser identified the unencrypted NTFS partition, decoded volume geometry, calculated the MFT location, and found the eight controlled files. Guest-VM exact byte lengths and parser logical sizes matched for all eight. Week 13 recovery again matched expected names and lengths.

| Known file | MFT record | Expected/recovered bytes | Length result |
|---|---:|---:|---|
| `Test.txt` | 38 | 83 | PASS |
| `Test2.txt` | 39 | 1,778 | PASS |
| `Testfile.docx` | 41 | 13,437 | PASS |
| `SunflowerTest.jpg` | 42 | 48,647 | PASS |
| `Thetestfile.pdf` | 43 | 17,247 | PASS |
| `WaterfallTest.png` | 44 | 277,325 | PASS |
| `HTMLtestdoc.html` | 55 | 608 | PASS |
| `JSON_test_File.json` | 56 | 579 | PASS |

**Important:** The original file-content SHA-256 hashes were not available. Recovered hashes were recorded, but byte-for-byte equivalence to independently recorded originals is **NOT VERIFIED**.

### 6.2 Alternate Data Stream recovery

The controlled host file `D:\ADS_Test\hostfile.txt` was found at MFT record 58. Its named resident `$DATA` stream `CapstoneEvidence` contained the 36-byte marker `CAPSTONE_ADS_TEST_20261001_Team3_001`. The recovered 36 bytes had SHA-256 `E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E`, matching the independently documented expected payload hash. **Result: PASS.**

### 6.3 Slack-space identification and recovery

For `Testfile.docx` (MFT record 41), the logical size was 13,437 bytes and allocated size 16,384 bytes, leaving **2,947 bytes** of final-cluster slack. The data run began at LCN 3659 and ended at LCN 3662; the slack began at absolute image offset **16,049,277**. A 25-byte marker, `TEAM3_SLACK_TEST_20261008`, was inserted into the first 25 bytes of that range in a working copy. The recovered payload SHA-256 was `3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2`, matching the original manifest. **Result: PASS.**

### 6.4 Integrity and regression

The November 15 regression log recorded **64 tests passing in 4.729 seconds**, with no failures or skips. The controlled working-image SHA-256 before and after recovery was identical: `D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7`. The Week 13 ADS, slack-range, bounded-slack, and source-preservation checks passed. The working image was not altered by these read-only extraction runs.

## 7. Discussion

The strongest outcome is independently checkable recovery of two deliberately planted payloads. The expected ADS and slack hashes were recorded in earlier manifests and matched the hashes computed from recovered outputs in Week 13. This provides stronger support than matching a filename or byte length alone. The source-image before/after hash comparison also supports the claim that recovery did not modify the controlled evidence image.

The parser's ability to handle resident attributes, nonresident extents, and a fragmented test file shows broader functionality than simple signature scanning. Defensive behavior—rejecting invalid records, unsafe output destinations, unsupported layouts, and inconsistent expectations—is particularly important in forensic software because silent guessing can produce misleading findings.

These results apply to the controlled test images and tested cases. They do not demonstrate universal support for all NTFS features, deleted-file reconstruction, every fragmented MFT layout, or recovery of unknown hidden content in arbitrary real-world images.


## 8. Conclusion

The team implemented and tested a Python-based NTFS forensic workflow that identifies partition and MFT structures, decodes file attributes and data runs, and recovers controlled named ADS and file-slack payloads from raw disk images. By November 15, 2026, the documented regression suite passed 64 tests, both hidden markers were recovered with matching original SHA-256 hashes, and the source working image remained unchanged during extraction. Eight known files were successfully identified and recovered at expected lengths, although exact content equivalence remains unverified without original hashes. The project demonstrates a useful foundation for reproducible, integrity-conscious NTFS forensic analysis and identifies clear next steps for broader validation.

## 9. References and evidence appendices

**Project evidence (repository-relative paths):**

- `docs/Baseline Evidence.md` — image provenance and SHA-256 register.
- `docs/week6_known_file_manifest.md` — eight known filenames, MFT records, and exact-size comparisons.
- `docs/week7_ads_payload_manifest.md` — original ADS marker and hash.
- `reports/evidence/week8/w8_slack_payload_manifest.json` — slack geometry, marker, and original hash.
- `reports/evidence/week13/image_validation.json` — recovered files, ADS, slack range, and image integrity.
- `reports/evidence/week13/slack_validation.json` — bounded slack extraction and hash comparison.
- `reports/evidence/week13/regression.txt` — 64-test regression log.
- `reports/weekly_report_13.md` — November 15 validation summary and screenshots.
- `reports/FORENSIC_EVIDENCE_CATALOG.md` — consolidated screenshot, hexdump, and hash index.
- `reports/evidence/week12/WEEK12_Slack_Space_Recovery_Test_Results.md` — slack workflow and supporting results.

