# Capstone Forensic Evidence Catalog

**Repository:** Lcurtis1Broncos/CSC-481-Capstone-Group  
**Purpose:** Consolidated index of committed screenshots, hashes, machine-readable reports, and payload byte representations, organized by the capstone task they support.

> Screenshots are linked to their original files in this repository. Hashes are transcribed from committed logs/manifests/reports, not recalculated here. Full disk images and recovered binary outputs are not stored in Git.

## Contents

1. [NTFS research and evidence format](#1-ntfs-research-and-evidence-format)
2. [Baseline image and NTFS validation](#2-baseline-image-and-ntfs-validation)
3. [Known-file and MFT validation](#3-known-file-and-mft-validation)
4. [ADS creation and parsing](#4-ads-creation-and-parsing)
5. [Slack-space marker placement](#5-slack-space-marker-placement)
6. [Parser validation](#6-parser-validation)
7. [File and ADS recovery](#7-file-and-ads-recovery)
8. [ADS positive and negative tests](#8-ads-positive-and-negative-tests)
9. [Bounded slack recovery](#9-bounded-slack-recovery)
10. [Hash register](#hash-register)
11. [Payload hexdumps](#payload-hexdumps)
12. [Evidence limitations](#evidence-limitations)

---

## 1. NTFS research and evidence format

**Task:** Research required NTFS on-disk structures and establish the evidence-log format.

- ![NTFS research](evidence/week3/w3_ntfs_research.png)
- ![NTFS definitions](evidence/week3/w3_ntfs_definitions.png)
- ![Evidence log template](evidence/week3/w3_evidence_log_template.png)
- ![NTFS image test](evidence/week3/w3_ntfs_image_test.png)
- ![Week 3 automated tests](evidence/week3/w3_automated_tests.png)

Related documents: ../docs/NTFS on disk structure research.md, ../docs/NTFS_structures_and_fields_definitions.md, ../docs/Evidence Log Format_template.md.

## 2. Baseline image and NTFS validation

**Task:** Create a clean NTFS baseline, identify its partition and boot sector, read MFT record 0, and compare parser output with Windows.

- ![Week 4 MFT record read](evidence/week4/w4_mft_record_read.png)
- ![Week 4 automated tests](evidence/week4/w4_automated_tests.png)
- ![NTFS partition identifier](evidence/week5/w5_ntfs_partition_identifier.png)
- ![NTFS boot sector fields](evidence/week5/w5_ntfs_boot_sector_fields.png)
- ![Full-disk MFT reader](evidence/week5/w5_full_disk_mft_reader.png)
- ![FSUtil NTFS information comparison](evidence/week5/w5_fsutil_ntfsinfo_comparison.png)
- ![Week 5 automated tests](evidence/week5/w5_automated_tests.png)

Recorded values: MBR partition 1 type 0x07; partition start LBA 2,048 (byte offset 1,048,576); 512 bytes/sector; 4,096 bytes/cluster; MFT record 0 at byte offset 3,222,274,048; volume serial 461C98171C9803D9.

See ../docs/Baseline Evidence.md for acquisition history and the distinction between the earlier BitLocker-protected image and the validated unencrypted image.

## 3. Known-file and MFT validation

**Task:** Add known files to the baseline, record the image hash, enumerate MFT records, and compare filenames and byte sizes.

- ![Files added and image hash](evidence/week6/w6_files_added_image_hash.png)
- ![MFT listing part 1](evidence/week6/w6_mft_file_listing_part1.png)
- ![MFT listing part 2](evidence/week6/w6_mft_file_listing_part2.png)
- ![VM baseline files](evidence/week6/w6_vm_baseline_files.png)
- ![Week 6 automated tests](evidence/week6/w6_automated_tests.png)

Related document: ../docs/week6_known_file_manifest.md. Later Week 9 evidence records that eight filenames and exact byte sizes matched the parser's unnamed DATA logical sizes.

## 4. ADS creation and parsing

**Task:** Create a named NTFS data stream, record its host, stream name, marker, length and hash, and validate parser output.

- ![Normal file attributes](evidence/week7/w7_attribute_summary_normal_file.png)
- ![ADS parser result](evidence/week7/w7_ads_parser_result.png)
- ![ADS parser host record](evidence/week7/w7_ads_parser_host_record.png)
- ![ADS stream information](evidence/week7/w7_ads_stream_info.png)
- ![ADS payload hash](evidence/week7/w7_ads_payload_hash.png)
- ![ADS image hash](evidence/week7/w7_ads_image_hash.png)
- ![ADS stream lengths](evidence/week7/w7_ads_stream_lengths.png)
- ![Week 7 automated tests](evidence/week7/w7_automated_tests.png)

| Field | Recorded value |
|---|---|
| Host file | D:\ADS_Test\hostfile.txt |
| Host MFT record | 58 |
| Stream name | CapstoneEvidence |
| Marker | CAPSTONE_ADS_TEST_20261001_Team3_001 |
| ADS length | 36 bytes |
| Unnamed DATA length | 31 bytes |
| ADS payload SHA-256 | E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E |
| ADS-created image SHA-256 | 2240CF8A1AA9D30231C39C4672DC51157093314950C4930EBBF5D30F5F59D2F5 |

See ../docs/week7_ads_payload_manifest.md and ../docs/ads_creation_workflow.md. The repository notes the image hash was independently calculated on 2026-10-03; the ADS payload hash was later matched by recovery reports.

## 5. Slack-space marker placement

**Task:** Identify a file's final-cluster slack region, place a controlled marker in a working copy, and preserve the source image.

- ![Data runs and slack location](evidence/week8/w8_data_runs_slack.png)
- ![Slack marker read-back](evidence/week8/w8_slack_marker_readback.png)
- ![Week 8 automated tests](evidence/week8/w8_automated_tests.png)

| Field | Recorded value |
|---|---|
| Host file | Testfile.docx |
| MFT record | 41 |
| Logical size | 13,437 bytes |
| Allocated size | 16,384 bytes |
| Cluster size | 4,096 bytes |
| Final LCN | 3,662 |
| Slack byte offset | 16,049,277 |
| Slack capacity | 2,947 bytes |
| Marker | TEAM3_SLACK_TEST_20261008 |
| Marker length | 25 bytes |
| Source image SHA-256 | 2240CF8A1AA9D30231C39C4672DC51157093314950C4930EBBF5D30F5F59D2F5 |
| Working image SHA-256 | D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7 |
| Marker SHA-256 | 3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2 |

The manifest says all output bytes match the source except the designated 25-byte payload range. See evidence/week8/w8_slack_payload_manifest.json.

## 6. Parser validation

**Task:** Compare parser output with the known-file image and verify file sizes, data runs, slack calculations and ADS metadata.

- ![Record 41 parser output](evidence/week9/w9_parser_record41.png)
- ![Slack and ADS parser output](evidence/week9/w9_parser_slack_ads.png)
- ![Exact VM file sizes](evidence/week9/w9_vm_exact_file_sizes.png)
- ![Week 9 automated tests](evidence/week9/w9_automated_tests.png)

Record 41 is Testfile.docx: logical size 13,437 bytes, allocated size 16,384 bytes, and slack length 2,947 bytes beginning at offset 16,049,277. Record 58 is hostfile.txt with 31-byte unnamed DATA and 36-byte resident CapstoneEvidence ADS.

Related document: ../docs/week9_validation.md.

## 7. File and ADS recovery

**Task:** Recover resident and nonresident file data and a named ADS, record output hashes, validate lengths, and prove the source image was not modified.

- ![Resident recovery](evidence/week10/w10_resident_recovery.png)
- ![Nonresident recovery](evidence/week10/w10_nonresident_recovery.png)
- ![ADS recovery](evidence/week10/w10_ads_recovery.png)
- ![Overwrite refusal](evidence/week10/w10_overwrite_refusal.png)
- ![Test command](evidence/week10/w10_automated_tests_command.png)
- ![45-test summary](evidence/week10/w10_automated_tests_summary.png)
- ![Integrated test command](evidence/week10/w10_integrated_tests_command.png)
- ![56-test summary](evidence/week10/w10_integrated_tests_summary.png)

Machine-readable records: evidence/week10/w10_recovery_validation.json, evidence/week10/w10_integrated_ads_report.json. Text logs: evidence/week10/w10_automated_tests.txt and evidence/week10/w10_integrated_tests.txt.

The integrated ADS report records 36 recovered bytes, matching expected/recovered payload hashes, and identical source hashes before and after. The eight baseline file outputs have recorded hashes and matching lengths, but original file hashes were not supplied; original-content equality is therefore unverified.

Related docs: ../docs/week10_recovery_support.md and week10_ads_recovery_report.md.

## 8. ADS positive and negative tests

**Task:** Demonstrate successful ADS recovery with the correct expected hash and rejection when the expected hash is intentionally wrong.

- ![ADS parser streams](evidence/week11/w11_parser_ads_streams.png)
- ![ADS recovery PASS](evidence/week11/w11_ads_recovery_pass.png)
- ![Wrong expected hash FAIL](evidence/week11/w11_ads_expected_hash_fail.png)
- ![Week 11 automated tests](evidence/week11/w11_automated_tests.png)

Machine-readable reports: evidence/week11/w11_ads_recovery_report.json and evidence/week11/w11_ads_negative_report.json.

The positive report records a 36-byte payload and matching expected/recovered hashes. The negative test is expected to report FAIL because the expected hash is wrong; this demonstrates correct rejection behavior. Both reports record identical source-image hashes before and after.

Related docs: evidence/week11/README.md and weekly_report_11.md.

## 9. Bounded slack-space recovery

**Task:** Recover the known marker from a bounded slack range, verify length/hash, preserve the source image, and test boundary conditions.

- ![Slack location](evidence/week12/w12_slack_location.png)
- ![Manual marker recovery](evidence/week12/w12_manual_marker_recovery.png)
- ![Integrated slack recovery PASS](evidence/week12/w12_slack_recovery_pass.png)
- ![64-test command](evidence/week12/w12_automated_tests_command.png)
- ![64-test summary](evidence/week12/w12_automated_tests_summary.png)

Machine-readable report: evidence/week12/w12_slack_recovery_report.json. Test log: evidence/week12/w12_automated_tests.txt. Implementation notes: ../docs/week12_slack_validation.md.

The integrated report records 25 recovered bytes, matching expected/recovered hashes, identical source hashes before and after, and overall PASS. The host file's logical size is 13,437 bytes; the full calculated slack capacity is 2,947 bytes; the payload is only 25 bytes.

---

## Hash register

Hashes are copied from the evidence log and machine-generated reports; they are not newly calculated here.

| Task / object | SHA-256 | Meaning / qualification |
|---|---|---|
| E-001 earlier BitLocker-protected image | 3815401D2D948B474D1EC104E2C5277ADD1D8DBFAAC4861388319A37EF235814 | Matched by second team member; unsuitable for NTFS parsing |
| E-002 clean unencrypted baseline | EFA4CA3DFA0127F7634EE71D59629A565DCEABB93B23A4A135C5B7AB84AE5E91 | Independently verified 2026-09-16 |
| E-003 eight-file validation image | 053D7CF98D07AAAEE265A1B4D027B384C528ABC55F1D59310B9BFDEE2CB76691 | Supplied hash; independent download-hash confirmation not recorded |
| E-004 ADS-created image | 2240CF8A1AA9D30231C39C4672DC51157093314950C4930EBBF5D30F5F59D2F5 | Independently calculated locally 2026-10-03 |
| ADS payload, CapstoneEvidence | E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E | 36-byte payload; later matched by recovery reports |
| E-005 ADS + slack working image | D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7 | Working image; before/after source-preservation checks match |
| Slack marker payload | 3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2 | 25-byte marker; matched by Week 12 recovery |
| Recovered Test.txt | D68EC557336622896727E44ED003136662FCD67CE8F9F57B23E70C0E09ADA797 | 83-byte output; no original hash supplied |
| Recovered Test2.txt | BA7F25F70009A6D45A9EF88C857C9C357856AA6D1201486DE9070522CFAEE64E | 1,778-byte output; no original hash supplied |
| Recovered Testfile.docx | 84A8A7AC155C36A5F4F9196A412D8DB16A6F12BD10794FEC362542E562DBE347 | 13,437-byte output; no original hash supplied |
| Recovered SunflowerTest.jpg | 658C1F66CE1C2D05B51F4E20044981228AAE39BE33B14737B5ADD448378B9E7C | 48,647-byte output; no original hash supplied |
| Recovered Thetestfile.pdf | 61FCC2B322094257A6B845E15D7AEFF99564E83260EA413DB05180DD8A0E3C8C | 17,247-byte output; no original hash supplied |
| Recovered WaterfallTest.png | 19CE26BC665962B8B6B766C48EFFC8676D1191B7B46CACD165418892ED42AA08 | 277,325-byte output; no original hash supplied |
| Recovered HTMLtestdoc.html | 815246781F0ADE404A0FECD2531CB027AB7F6C1177868967BC7CCA47D88AE0FB | 608-byte output; no original hash supplied |
| Recovered JSON_test_File.json | 65EAF0824C357D4FC9955E75CA29CF3F6476DCB0374241DAB08C3714991E8D34 | 579-byte output; no original hash supplied |
| Recovered ADS output | E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E | 36-byte recovered stream; expected hash matches |
| Recovered slack marker | 3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2 | 25-byte recovered marker; expected hash matches |

## Payload hexdumps

### Week 7 ADS marker — 36 bytes

Recorded ASCII/UTF-8 marker, without a newline:

CAPSTONE_ADS_TEST_20261001_Team3_001

```text
43 41 50 53 54 4F 4E 45 5F 41 44 53 5F 54 45 53 54 5F
32 30 32 36 31 30 30 31 5F 54 65 61 6D 33 5F 30 30 31
```

### Week 8 / Week 12 slack marker — 25 bytes

Recorded UTF-8 marker, no BOM and no newline:

TEAM3_SLACK_TEST_20261008

```text
54 45 41 4D 33 5F 53 4C 41 43 4B 5F 54 45 53 54 5F
32 30 32 36 31 30 30 38
```

### Original slack bytes overwritten — 25 bytes

The Week 8 JSON manifest records the original 25-byte range as all zero bytes:

```text
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00
```

These are payload-byte representations from the committed marker strings and the manifest's original_slack_bytes_hex field. They are not full disk or full-cluster hexdumps.

## Evidence limitations

1. Full .dd images and recovered binary outputs are excluded from Git; only evidence metadata, reports, hashes and screenshots are stored.
2. No standalone .hex or .dump files appear in the repository tree. The slack manifest contains the 25 overwritten bytes as hex; marker hexdumps above are byte encodings of the recorded marker strings. Terminal hex views, if present in screenshots, remain in the original screenshots.
3. The Week 10 report explicitly says original hashes for the eight baseline files were not supplied. Recovered output hashes and matching lengths do not prove original-content equality.
4. The ADS payload hash is recorded in the Week 7 manifest and later matches recovered ADS output in Weeks 10 and 11.
5. The slack payload hash matches in the Week 8 manifest and Week 12 integrated recovery report. The working image's before/after hashes match.
6. Week 11's wrong-expected-hash FAIL is an expected negative-test result, not a failed positive recovery.
7. Preserve attribution in the weekly evidence notes: some screenshots and runs were supplied/performed by Jeff, some by Lucas, and some are automated/agent-run checks.

## Source records

- ../docs/Baseline Evidence.md
- ../docs/Evidence Log Format_template.md
- ../docs/week7_ads_payload_manifest.md
- evidence/week8/w8_slack_payload_manifest.json
- evidence/week10/w10_recovery_validation.json
- evidence/week10/w10_integrated_ads_report.json
- evidence/week11/w11_ads_recovery_report.json
- evidence/week12/w12_slack_recovery_report.json
- weekly_report_12.md
