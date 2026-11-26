# Final Forensic Evidence Log

**Project:** NTFS Filesystem Steganography and Forensic MFT Parser  
**Course / team:** CSC-481 Capstone / Team 3  
**Prepared:** November 17, 2026  
**Updated:** November 26, 2026

**Status:** Complete for the recorded controlled experiments; unrecorded custody fields remain explicitly identified.
**Scope:** Controlled VirtualBox NTFS images, parser validation, ADS recovery, and file-slack recovery.


## 1. Evidence handling and scope

The team used dedicated controlled virtual disks and read-only parsing/recovery utilities. Slack-marker insertion was performed on a separate working copy. The original controlled ADS image was preserved. Evidence IDs below track distinct image states; hashes must not be treated as interchangeable between those states.

**Chain-of-custody fields for each image:** evidence ID, source device/VM, acquisition date and time with timezone, collector, acquisition command/tool and version, original image filename, original location, SHA-256, verification operator and time, transfer/storage location, and subsequent access/processing history. Where source documentation does not supply a field, mark it **Not recorded**, not inferred.

## 2. Image evidence register

| ID | Image / role | Date recorded | SHA-256 | Verification / disposition |
|---|---|---|---|---|
| E-001 | `NTFS_Forensic_Baseline_RAW.dd` — initial BitLocker-protected image | Sep 11–12, 2026 | `3815401D2D948B474D1EC104E2C5277ADD1D8DBFAAC4861388319A37EF235814` | Lucas acquired; Jeff verified hash. Partition had `-FVE-FS-` header; excluded from NTFS parsing. |
| E-002 | `NTFS_Forensic_Baseline_Unencrypted_RAW.dd` — clean unencrypted baseline | Sep 16, 2026 | `EFA4CA3DFA0127F7634EE71D59629A565DCEABB93B23A4A135C5B7AB84AE5E91` | Lucas acquired; Jeff independently verified. |
| E-003 | `NTFS_Forensic_Baseline_Unencrypted_FilesAdded_RAW.dd` — eight known files | Week 6 | `053D7CF98D07AAAEE265A1B4D027B384C528ABC55F1D59310B9BFDEE2CB76691` | Lucas supplied hash; independent image-hash confirmation not recorded. |
| E-004 | `NTFS_Forensic_Baseline_ADS_Created_RAW.dd` — controlled ADS | Oct 3 validation | `2240CF8A1AA9D30231C39C4672DC51157093314950C4930EBBF5D30F5F59D2F5` | Lucas acquired; Jeff independently verified image hash. |
| E-005 | `NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd` — ADS and slack marker | Oct 8; checked Nov 15 | `D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7` | Working copy from E-004. Nov 15 before/after hash matched; source unchanged during recovery. |

**Image storage:** Team transfer/local lab storage; large RAW images excluded from GitHub. **Exact final storage locations, access permissions, transfer history, and retention plan:** require team confirmation.

## 3. NTFS partition and metadata evidence

| Field | Validated value | Source |
|---|---|---|
| Partition style | MBR | Baseline evidence / midterm report |
| NTFS partition type | `0x07` | Week 5 validation |
| Partition start LBA | 2,048 | Week 5 validation |
| Partition byte offset | 1,048,576 | Week 5 validation |
| Bytes per sector | 512 | Week 5 validation |
| Bytes per cluster | 4,096 | Week 5 validation |
| MFT start LCN | 786,432 | Week 5 validation |
| MFT mirror LCN | 2 | Week 5 validation |
| MFT record size | 1,024 bytes | Week 5 validation |
| Absolute first MFT offset | 3,222,274,048 | Week 5 validation |
| Volume serial | `461C98171C9803D9` | Week 5 validation |

**Result:** Parser geometry and MFT location matched Windows `fsutil fsinfo ntfsinfo D:` in the controlled VM. The early practice image `7-ntfs-undel.dd` has different geometry and must not be conflated with the project baseline.

## 4. Known-file validation (E-003/E-005)

Guest VM exact byte lengths were compared with parsed `$DATA` logical lengths; Week 13 recovered lengths matched for all eight files. On November 25, Jeff confirmed that all eight original-file hashes match the recorded recovered hashes. The [dated comparison record](../docs/baseline_hash_verification.md) supplies the values and provenance. Original command output was not attached.

| File | MFT | Expected / recovered bytes | Name and size | Original-content SHA-256 comparison |
|---|---:|---:|---|---|
| `Test.txt` | 38 | 83 | PASS | MATCH — team-confirmed Nov 25 |
| `Test2.txt` | 39 | 1,778 | PASS | MATCH — team-confirmed Nov 25 |
| `Testfile.docx` | 41 | 13,437 | PASS | MATCH — team-confirmed Nov 25 |
| `SunflowerTest.jpg` | 42 | 48,647 | PASS | MATCH — team-confirmed Nov 25 |
| `Thetestfile.pdf` | 43 | 17,247 | PASS | MATCH — team-confirmed Nov 25 |
| `WaterfallTest.png` | 44 | 277,325 | PASS | MATCH — team-confirmed Nov 25 |
| `HTMLtestdoc.html` | 55 | 608 | PASS | MATCH — team-confirmed Nov 25 |
| `JSON_test_File.json` | 56 | 579 | PASS | MATCH — team-confirmed Nov 25 |


## 5. ADS evidence — controlled payload

| Field | Recorded value |
|---|---|
| Evidence ID | ADS-001; image E-004 / recovered from E-005 |
| Host | `D:\ADS_Test\hostfile.txt` |
| MFT record | 58 |
| Named `$DATA` stream | `CapstoneEvidence` |
| Storage type | Resident |
| Marker | `CAPSTONE_ADS_TEST_20261001_Team3_001` |
| Payload length | 36 bytes |
| Expected and recovered SHA-256 | `E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E` |
| Week 13 outcome | PASS — exact length and expected hash matched |

**Source:** `docs/week7_ads_payload_manifest.md`; `reports/evidence/week13/image_validation.json`. The original Week 7 manifest predates recovery; the Week 13 result supplies the later recovery verification.

## 6. File-slack evidence — controlled payload

| Field | Recorded value |
|---|---|
| Evidence ID | SLACK-001; image E-005 |
| Host file | `Testfile.docx` |
| MFT record | 41 |
| Host logical size | 13,437 bytes |
| Allocated size | 16,384 bytes |
| Cluster size | 4,096 bytes |
| Data run | Start LCN 3659; 4 clusters |
| Final LCN | 3662 |
| Slack image start offset | 16,049,277 decimal (`0x00F4E47D`) |
| Available file slack | 2,947 bytes |
| Marker | `TEAM3_SLACK_TEST_20261008` |
| Marker encoding | UTF-8, no BOM or newline |
| Marker length | 25 bytes |
| Expected and recovered SHA-256 | `3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2` |
| Extraction | 25 bytes from beginning of calculated slack range |
| Week 13 outcome | PASS — length/hash match; image unchanged |

**Calculation:** `16,384 - 13,437 = 2,947` bytes of slack. The marker occupies the first 25 bytes, not the entire slack region. The Week 8 embedding manifest records the pre-insertion bytes and states that only the designated marker range changed in the working copy.

## 7. Regression and validation summary

| Check | Evidence | Result |
|---|---|---|
| Unit/regression suite, Nov 15 | `reports/evidence/week13/regression.txt` | PASS — 64 tests, 4.729 s, no failures or skips |
| Eight recovered files, Nov 15 | `reports/evidence/week13/image_validation.json` | PASS for names/lengths; original-hash comparison pending at that time |
| Original-file hash follow-up, Nov 25 | `reports/evidence/final_report/baseline_hash_confirmation.json` | 8/8 original/recovered hash matches, team-confirmed |
| ADS extraction | `reports/evidence/week13/image_validation.json` | PASS, 36 bytes and matching original SHA-256 |
| Slack range calculation | `reports/evidence/week13/image_validation.json` | PASS, offset 16,049,277 and 2,947-byte range |
| Bounded slack extraction | `reports/evidence/week13/slack_validation.json` | PASS, 25 bytes and matching original SHA-256 |
| Working image preservation | Both Week 13 JSON reports | PASS, same expected before/after SHA-256 |

## 8. Screenshot and artifact index

- NTFS boot sector and partition geometry: `reports/evidence/week5/w5_ntfs_boot_sector_fields.png`, `w5_ntfs_partition_identifier.png`, `w5_fsutil_ntfsinfo_comparison.png`.
- Known files / MFT: `reports/evidence/week6/w6_mft_file_listing_part1.png`, `w6_mft_file_listing_part2.png`, `reports/evidence/week9/w9_vm_exact_file_sizes.png`.
- ADS creation / parsing: `reports/evidence/week7/w7_ads_stream_info.png`, `w7_ads_payload_hash.png`, `w7_ads_parser_result.png`.
- Slack location / recovery: `reports/evidence/week12/w12_slack_location.png`, `w12_manual_marker_recovery.png`, `w12_slack_recovery_pass.png`.
- Final regression / recovery: `reports/evidence/week13/w13_regression.png`, `w13_ads_validation.png`, `w13_slack_validation.png`.
- Additional indexed screenshots and payload hexdumps: `reports/FORENSIC_EVIDENCE_CATALOG.md`.

Screenshot descriptions are based on repository documentation and filenames; no independent visual pixel inspection was performed for this draft.

## 9. Primary repository sources

- `docs/Baseline Evidence.md`
- `docs/week6_known_file_manifest.md`
- `docs/week7_ads_payload_manifest.md`
- `reports/evidence/week8/w8_slack_payload_manifest.json`
- `reports/evidence/week13/image_validation.json`
- `reports/evidence/week13/slack_validation.json`
- `reports/evidence/week13/regression.txt`
- `reports/weekly_report_13.md`
- `reports/FORENSIC_EVIDENCE_CATALOG.md`

## November 25 Detection Experiment

Added [100 labeled synthetic screening cases](evidence/final_detection/README.md),
with per-image hashes, labels, decisions and measured detection/evasion rates.
All synthetic sources were unchanged. Two known Windows positives were also
flagged; the complete working-image hash matched before and after screening.
The 73-test current-branch log is saved separately from historical release logs.

