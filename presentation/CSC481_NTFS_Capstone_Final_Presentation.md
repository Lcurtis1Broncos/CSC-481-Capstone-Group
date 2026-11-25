# CSC 481 Capstone — Final Presentation

## Slide index

- [Slide 01 — Finding Hidden Data in NTFS](#slide-01--finding-hidden-data-in-ntfs)
- [Slide 02 — The Problem: Hidden Data Beyond Normal Files](#slide-02--the-problem-hidden-data-beyond-normal-files)
- [Slide 03 — Project Goals and Success Criteria](#slide-03--project-goals-and-success-criteria)
- [Slide 04 — Controlled Lab and Evidence Workflow](#slide-04--controlled-lab-and-evidence-workflow)
- [Slide 05 — What the Parser Understands](#slide-05--what-the-parser-understands)
- [Slide 06 — Baseline Image: Forensic Geometry](#slide-06--baseline-image-forensic-geometry)
- [Slide 07 — Evidence Image Lineage](#slide-07--evidence-image-lineage)
- [Slide 08 — Experiment 1: Alternate Data Stream](#slide-08--experiment-1-alternate-data-stream)
- [Slide 09 — Experiment 2: File Slack Recovery](#slide-09--experiment-2-file-slack-recovery)
- [Slide 10 — How Recovery Was Verified](#slide-10--how-recovery-was-verified)
- [Slide 11 — Week 13: Final Recorded Test Campaign](#slide-11--week-13-final-recorded-test-campaign)
- [Slide 12 — Important Limitations and Honest Claims](#slide-12--important-limitations-and-honest-claims)
- [Slide 13 — Engineering and Forensic Lessons](#slide-13--engineering-and-forensic-lessons)
- [Slide 14 — Project Outcome and Next Steps](#slide-14--project-outcome-and-next-steps)
- [Slide 15 — Evidence and Source Documents](#slide-15--evidence-and-source-documents)
- [Slide 16 — Questions?](#slide-16--questions)

---

## Slide 01 — Finding Hidden Data in NTFS

Filesystem steganography, raw-disk parsing, and evidence-based recovery

From a controlled disk image to reproducible forensic findings

Team 3  |  Lucas Curtis & Jeff Perez  |  Fall 2026

---

## Slide 02 — The Problem: Hidden Data Beyond Normal Files

### Alternate Data Streams (ADS)

NTFS can associate named $DATA streams with a file. Their content may not appear in an ordinary file listing.

### File Slack Space

The unused portion of a file’s final allocated cluster may contain bytes not visible in the logical file content.

Investigative question: Can we locate, extract, and verify known hidden payloads without changing the evidence image?

---

## Slide 03 — Project Goals and Success Criteria

- Build a read-only parser for NTFS disk images and MFT records
- Decode filesystem structures, attributes, and nonresident data runs
- Identify controlled ADS and file-slack payload locations
- Recover resident, nonresident, ADS, and bounded slack data
- Verify outputs using expected lengths, SHA-256 hashes, and regression tests

---

## Slide 04 — Controlled Lab and Evidence Workflow

**VirtualBox** (NTFS lab disk) → **RAW image** (Preserved .dd) → **Python parser** (MBR + MFT) → **Recovery tool** (Read-only export) → **Validation** (SHA-256 + tests)

Separate working-image copies were used for controlled payload embedding; forensic reads and exports were performed without modifying the source image.

---

## Slide 05 — What the Parser Understands

| Item | Details |
|---|---|
| MBR / NTFS boot | Partition offset, sector and cluster geometry |
| MFT records | Record signatures, file names, metadata |
| $DATA attributes | Resident data, named ADS, nonresident extents |
| Data runs / slack | Fragment mapping and final-cluster unused bytes |

---

## Slide 06 — Baseline Image: Forensic Geometry

| Item | Details |
|---|---|
| Disk size | 8 GiB |
| Partition start | LBA 2,048 / 1,048,576 bytes |
| Sector / cluster | 512 / 4,096 bytes |
| MFT record | 1,024 bytes |
| First MFT offset | 3,222,274,048 bytes |
| Volume serial | 461C98171C9803D9 |

---

## Slide 07 — Evidence Image Lineage

| Evidence ID | Image | Finding |
|---|---|---|
| E-001 | BitLocker baseline | Retained; not usable for NTFS parsing |
| E-002 | Unencrypted baseline | Validated NTFS boot and MFT |
| E-003 | Eight-file image | Known-file name and size checks |
| E-004 | ADS-created image | Named stream and 36-byte marker |
| E-005 | ADS + slack working | 25-byte slack marker and recovery |

---

## Slide 08 — Experiment 1: Alternate Data Stream

### Controlled payload

- Host: hostfile.txt  •  MFT record 58
- Stream: CapstoneEvidence
- Marker: CAPSTONE_ADS_TEST_20261001_Team3_001
- Payload: 36 bytes

### Forensic outcome

Parser identified the named resident $DATA attribute. Recovery produced 36 bytes with a SHA-256 matching the independently recorded payload value.

SHA-256  E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E

---

## Slide 09 — Experiment 2: File Slack Recovery

### Target file

- Testfile.docx  •  MFT record 41
- Logical size: 13,437 bytes
- Allocated size: 16,384 bytes
- Cluster size: 4,096 bytes
- Final cluster: LCN 3,662

### Bounded extraction

- Slack start: image byte 16,049,277
- Available slack: 2,947 bytes
- Known marker: 25 bytes
- Recovered: 25 bytes
- Expected SHA-256: matched

Slack calculation: 16,384 allocated − 13,437 logical = 2,947 unused bytes

---

## Slide 10 — How Recovery Was Verified

| Item | Details |
|---|---|
| 1  Locate | Parse MFT, attributes, and data runs |
| 2  Extract | Export only the requested stream or slack range |
| 3  Compare | Check byte count and original SHA-256 |
| 4  Preserve | Verify source-image hash before and after |

---

## Slide 11 — Week 13: Final Recorded Test Campaign

| Item | Details |
|---|---|
| 64 / 64 | Regression tests passed |
| 8 / 8 | File names + lengths matched |
| 2 / 2 | Known payload hashes matched |
| Source image unchanged | SHA-256 before = SHA-256 after |

Evidence: November 15 regression.txt, image_validation.json, slack_validation.json

---

## Slide 12 — Important Limitations and Honest Claims

### Verified

Known ADS and slack payloads matched expected byte counts and original SHA-256 values. The working image remained unchanged during validation.

### Not yet verified

The eight recovered baseline files match expected names and sizes, but independently recorded original content hashes are unavailable.

Additional follow-up: earlier milestone requested at least 10 known files; current documented controlled set contains 8.

---

## Slide 13 — Engineering and Forensic Lessons

- Filesystem metadata can reveal content not shown in ordinary file views.
- Resident and nonresident data require different extraction logic.
- Data-run decoding matters when files are fragmented.
- Expected lengths alone do not prove byte-for-byte integrity.
- Reproducible tests, failure handling, and hashes make findings defensible.

---

## Slide 14 — Project Outcome and Next Steps

### What we demonstrated

A read-only NTFS parser and recovery workflow can locate and recover controlled ADS and file-slack payloads with matching SHA-256 evidence.

### What remains

Obtain original hashes for the eight baseline files; expand the validation set if required; finalize evidence custody details and report/presentation review.

Bottom line: we connected filesystem structure → hidden bytes → recovery → independent verification.

---

## Slide 15 — Evidence and Source Documents

- docs/Baseline Evidence.md  •  image lineage and SHA-256 register
- docs/week6_known_file_manifest.md  •  eight-file validation
- docs/week7_ads_payload_manifest.md  •  controlled ADS
- reports/evidence/week8/w8_slack_payload_manifest.json  •  slack marker
- reports/evidence/week13/  •  regression and recovery validation
- reports/FORENSIC_EVIDENCE_CATALOG.md  •  screenshot index

---

## Slide 16 — Questions?

NTFS Filesystem Steganography & Forensic MFT Parser

Evidence-based recovery of hidden ADS and slack-space payloads

Repository: github.com/Lcurtis1Broncos/CSC-481-Capstone-Group
