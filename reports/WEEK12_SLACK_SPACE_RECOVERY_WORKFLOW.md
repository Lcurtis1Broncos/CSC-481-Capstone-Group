# NTFS Slack Space Recovery Workflow — Week 12

**Evidence ID:** `TEAM3-SLACK-RECOVERY`  
**Project:** CSC-481 Capstone, Team 3  
**Workflow status:** <span>PASS</span>  
**Primary analyst for recovery and validation:** Jeff Perez  
**Workflow documentation:** Lucas Curtis  
**Reporting period:** November 2–8, 2026  
**Integrated recovery report created:** November 6, 2026 at 17:26:44 UTC

## Purpose and scope

This document records the Week 12 controlled recovery of a known 25-byte test marker from the slack space associated with `Testfile.docx`. It follows the structure of the team's Slack Space Recovery Workflow Template and incorporates the machine-generated `w12_slack_recovery_report.json` and the Week 12 team progress report.

The task was a **known-range, bounded slack-payload recovery test**. It did not attempt automatic discovery of arbitrary hidden data, and it did not export the entire 2,947-byte slack region.

## 1. Preserve the NTFS Evidence Image

### Procedure

1. Use the controlled working RAW image as the recovery source.
2. Record its SHA-256 before recovery.
3. Perform recovery using read-only source-image access and write the recovered bytes to a separate output file.
4. Calculate the source image SHA-256 after recovery.
5. Compare the before/after values with the expected working-image hash.

### Evidence tracking

| Field | Recorded value |
|---|---|
| Evidence ID | `TEAM3-SLACK-RECOVERY` |
| Original image filename | Original acquisition filename not recorded in the Week 12 report |
| Source/working image filename | `NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd` |
| Original image size (bytes) | Not recorded in the Week 12 source documents |
| Working image size (bytes) | Not recorded in the Week 12 source documents |
| Original SHA-256 | Not separately recorded for this recovery run |
| Source/working image SHA-256 before | `D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7` |
| Source/working image SHA-256 after | `D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7` |
| Expected working-image SHA-256 | `D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7` |
| Image creation date | Not recorded in the Week 12 source documents |
| Working copy creation date | Not recorded in the Week 12 source documents |
| Recovery source path in report | `NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd` |
| Analyst | Jeff Perez |

**Result:** PASS. The source hash matched the expected working-image hash, and the before/after hashes were identical. The report records `source_image_hash_match: true` and `source_unchanged: true`.

**Integrity note:** The Week 12 report establishes that the image used for this recovery was unchanged. It does not provide a separate original-acquisition image hash or image byte size; those values are intentionally left unspecified.

## 2. Identify NTFS Partitions

The Week 12 recovery report identifies the source as an NTFS working image and records the target MFT record and byte offsets. It does not reproduce the partition table or complete NTFS volume geometry.

### Evidence tracking

| Field | Recorded value |
|---|---|
| Evidence ID | `TEAM3-SLACK-RECOVERY` |
| Image filename | `NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd` |
| Partition number | Not recorded in the Week 12 source documents |
| Partition starting sector | Not recorded in the Week 12 source documents |
| Partition offset (bytes) | Not recorded in the Week 12 source documents |
| Partition size (bytes) | Not recorded in the Week 12 source documents |
| Sector size (bytes) | Not recorded in the Week 12 source documents |
| Cluster size (bytes) | 4,096 |
| NTFS volume label | Not recorded in the Week 12 source documents |
| Filesystem type | NTFS |
| Tool used | `ntfs_recovery.py` (stream and bounded-slack reporting) |
| Date examined | November 3–6, 2026 |

**Note:** The 4,096-byte cluster size is consistent with the Week 12 validation's 16,384-byte allocation spanning four clusters. Partition geometry is not inferred here because it is not included in the two source documents used for this report.

## 3. Identify Files and MFT Records

The selected file was `Testfile.docx`, identified in MFT record 41. The weekly report states that the file has 13,437 logical bytes and one 16,384-byte allocated extent beginning at image offset 16,035,840.

### Evidence tracking

| Field | Recorded value |
|---|---|
| Evidence ID | `TEAM3-SLACK-RECOVERY` |
| Original filename | `Testfile.docx` |
| File path | Full host path not recorded; file is identified by name in the NTFS image |
| File extension | `.docx` |
| File class | Document |
| MFT record number | 41 |
| MFT record byte offset | 3,222,316,032 |
| Original/logical file size (bytes) | 13,437 |
| Allocation status | Allocated extent reported; file identified in MFT record 41 |
| Data attribute type | Nonresident (`resident: false` in the recovery report) |
| Allocated extent | Starts at image offset 16,035,840; length 16,384 bytes |
| Allocated cluster count | 4 |
| Tool used | `ntfs_recovery.py` |
| Date identified | November 3, 2026 |

The recovery report's `logical_size: 25` describes the selected slack-payload recovery extent. It is **not** the logical size of the host document. The host document's logical size is separately recorded as 13,437 bytes.

## 4. Locate Slack Space

### Calculation and observed location

The final allocated cluster is LCN 3662. The host file's logical content ends at the following image byte offset:

```text
Allocated extent start     16,035,840
Host logical file size          13,437
                            ----------
Slack start offset          16,049,277
```

The full slack capacity is 2,947 bytes. The test payload occupies the first 25 bytes of that slack range.

### Evidence tracking

| Field | Recorded value |
|---|---|
| Evidence ID | `TEAM3-SLACK-RECOVERY` |
| Original filename | `Testfile.docx` |
| MFT record number | 41 |
| Host file logical size (bytes) | 13,437 |
| Cluster size (bytes) | 4,096 |
| Allocated cluster count | 4 |
| Final cluster number (LCN) | 3662 |
| Expected/full slack size (bytes) | 2,947 |
| Slack start image offset (bytes) | 16,049,277 |
| Slack-relative payload offset | 0 |
| Payload range | Image offsets 16,049,277–16,049,301 inclusive |
| Tool used | `ntfs_recovery.py` and manual read-only extraction |
| Date identified | November 3, 2026 |

**Boundary distinction:** The full slack range is 2,947 bytes. The recovered test marker is only 25 bytes, leaving 2,922 bytes of slack outside the selected payload. The recovery utility maps the final logical cluster through the file's data runs; it does not rely on assuming that all files are physically contiguous.

## 5. Extract Slack Space

### Manual extraction — November 4

Jeff opened the controlled working image read-only, sought to the manifest's documented slack offset, read exactly 25 bytes, and saved them to a new output file using create-new behavior. The output displayed the expected marker:

```text
TEAM3_SLACK_TEST_20261008
```

This manual step extracted only the known 25-byte payload, not the entire slack range.

### Integrated bounded recovery — November 6

The integrated recovery/report utility used MFT record 41 and the bounded option `--slack-length 25`. It derived the slack location from validated file metadata and wrote the result to a separate output path.

### Evidence tracking

| Field | Recorded value |
|---|---|
| Evidence ID | `TEAM3-SLACK-RECOVERY` |
| Original filename | `Testfile.docx` |
| MFT record number | 41 |
| Extracted filename | `w12_slack_marker.bin` |
| Extraction method | Manual read-only extraction; integrated bounded slack recovery |
| Extraction tool | `ntfs_recovery.py` (stream and bounded slack reporting); manual read-only image read |
| Tool version | Not recorded in the Week 12 source documents |
| Extracted byte length | 25 |
| Manual extraction date | November 4, 2026 |
| Integrated report timestamp | November 6, 2026, 17:26:44 UTC |
| Repository-relative output location | `reports/evidence/week12/recovered/w12_slack_marker.bin` |
| Extraction status | PASS |
| Analyst credited for manual recovery | Jeff Perez |

The JSON report records the original Windows output path under Jeff's working directory. The repository-relative location above identifies the corresponding Week 12 evidence location without repeating a personal workstation path.

## 6. Analyze Recovered Data

### Evidence tracking

| Field | Recorded value |
|---|---|
| Evidence ID | `TEAM3-SLACK-RECOVERY` |
| Extracted filename | `w12_slack_marker.bin` |
| Recovered byte length | 25 |
| File signature identified | No file signature reported; payload is a text marker |
| Recovered text | `TEAM3_SLACK_TEST_20261008` |
| Test marker identified | Yes — exact expected marker |
| Artifact type | Controlled ASCII/UTF-8 test marker |
| Hexadecimal image offset | `0x00F4D27D` (decimal 16,049,277) |
| Slack-relative offset | 0 |
| Analysis tool | Manual read-back and `ntfs_recovery.py` integrated recovery/report workflow |
| Analysis findings | Recovered marker is 25 bytes and matches the known test payload hash |
| Date analyzed | November 4 and November 6, 2026 |
| Analyst | Jeff Perez |

The recovery report records the selected payload extent at image offset 16,049,277 with a length of 25 bytes. The weekly report records that the manual read-back displayed the expected marker. The hash comparison below establishes exact-byte agreement with the known payload.

## 7. Validate and Document Findings

### Hash and length comparison

| Validation field | Expected | Recovered | Result |
|---|---:|---:|---|
| Payload byte length | 25 | 25 | MATCH |
| Payload SHA-256 | `3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2` | `3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2` | MATCH |
| Source image SHA-256 | `D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7` | `D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7` | MATCH |
| Source unchanged | `true` | `true` | PASS |

### Evidence tracking

| Field | Recorded value |
|---|---|
| Evidence ID | `TEAM3-SLACK-RECOVERY` |
| Original filename | `Testfile.docx` |
| Recovered filename | `w12_slack_marker.bin` |
| Host original file size (bytes) | 13,437 |
| Full calculated slack size (bytes) | 2,947 |
| Recovered payload size (bytes) | 25 |
| Recovered artifact SHA-256 | `3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2` |
| Expected payload SHA-256 | `3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2` |
| Hash match status | MATCH |
| Test marker match status | MATCH |
| Validation result | PASS |
| Discrepancies | No payload length/hash discrepancy reported. Original-acquisition image hash, image sizes, partition geometry, and tool version are not provided in the Week 12 source documents. |
| Recovery report location | `reports/evidence/week12/w12_slack_recovery_report.json` |
| Validation date | November 6, 2026 |
| Reviewing analyst | Not separately identified in the source report |
| Final evidence status | PASS — known 25-byte payload recovered and verified; source image unchanged |

### Overall finding

The Week 12 integrated recovery report records `overall_result: PASS`, no errors, a 25-byte recovered payload, matching expected and recovered SHA-256 hashes, a matching expected source-image hash, and identical source-image hashes before and after recovery.

The positive result demonstrates successful recovery of the known marker from a bounded slack range. It does not demonstrate automatic discovery of unknown hidden payloads, and it does not establish original-content hash equality for the eight baseline files whose independent original hashes remain unavailable.

## Regression and safety validation

The Week 12 progress report records that the expanded test suite included eight new slack-recovery tests and that all 64 tests passed. Jeff's November 6 personal rerun completed in 4.741 seconds with no failures or skips.

The new tests covered:

- Correct mapping of the final fragment for a fragmented file.
- Relative-offset and exact-end reads.
- Rejection of zero or negative lengths and reads beyond the slack boundary.
- Resident, empty, and cluster-aligned stream cases.
- Refusal to overwrite an existing output.
- Actual command-line recovery behavior.
- Correct FAIL behavior when an expected payload hash is intentionally wrong.
- Refusal of invalid ranges before output/report files are created.

The weekly report distinguishes synthetic negative-test cases from the real-image positive recovery. The real-image report in this document is a positive PASS result.

## Evidence handling and chain of custody

- The recovery source was opened read-only; the recovered artifact was written separately.
- The output path used a new file rather than overwriting an existing artifact.
- The source-image SHA-256 was recorded before and after processing and remained identical.
- The recovered payload's length and SHA-256 were compared with the original Week 8 payload manifest values.
- The machine-generated JSON report and the weekly report should be retained alongside the recovered output and screenshots.

**Chain-of-custody limitation:** The Week 12 source documents do not provide a complete transfer log, evidence storage access log, or signatures for each custody event. Those details should be added if required by the capstone's formal evidence-handling standard.

## Final deliverables and references

| Deliverable | Location or status |
|---|---|
| NTFS working evidence image | `NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd` (kept outside Git) |
| Slack location screenshot | `reports/evidence/week12/w12_slack_location.png` |
| Manual marker recovery screenshot | `reports/evidence/week12/w12_manual_marker_recovery.png` |
| Integrated recovery PASS screenshot | `reports/evidence/week12/w12_slack_recovery_pass.png` |
| Recovered marker | `reports/evidence/week12/recovered/w12_slack_marker.bin` (recovered output; binary output may be excluded from Git) |
| Machine-generated recovery report | `reports/evidence/week12/w12_slack_recovery_report.json` |
| Automated test screenshots | `reports/evidence/week12/w12_automated_tests_command.png` and `w12_automated_tests_summary.png` |
| Original marker manifest | `reports/evidence/week8/w8_slack_payload_manifest.json` |
| Workflow template | `docs/Slack Space Recovery Workflow Template.md` |
| Weekly progress report | `reports/weekly_report_12.md` |

### Source documents used

1. `docs/Slack Space Recovery Workflow Template.md` — workflow sections and evidence-tracking fields.
2. `reports/evidence/week12/w12_slack_recovery_report.json` — machine-generated offsets, lengths, hashes, recovery status, and source-image integrity values.
3. `reports/weekly_report_12.md` — manual extraction procedure, dates, marker text, test results, implementation limits, and team contributions.

---

**Conclusion:** The known 25-byte Week 8 slack marker was successfully recovered from the calculated slack region of `Testfile.docx` (MFT record 41). The recovered length and SHA-256 matched the expected payload, and the source working image remained unchanged. The result is a verified bounded slack-payload recovery, not a general-purpose hidden-data discovery result.
