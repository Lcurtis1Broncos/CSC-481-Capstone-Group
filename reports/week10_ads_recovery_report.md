# Week 10 ADS Recovery Report

## Test information

- **Test ID:** W10-ADS-RECOVERY-01
- **Recovery date:** October 23, 2026
- **Report prepared:** October 24, 2026
- **Person running the recovery:** Jeff Perez
- **Workflow and report-template author:** Lucas Curtis, GitHub commit `3f5339d`
- **Tool:** `code/ntfs_recovery.py`, local Week 10 implementation; not yet committed
- **Test status:** PASS for recovered payload length and original SHA-256 comparison

This completed team report uses Lucas's
[workflow and report format](../docs/ADS%20Recovery%20Workflow.md) and Jeff's
recorded recovery run. No recovery run by Lucas is claimed.

## Source image

- **Name:** `NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd`
- **Path used:** Repository root, supplied as the filename above
- **Recorded SHA-256:**
  `D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7`

The [October 21 validation](evidence/week10/w10_recovery_validation.json)
measured that full-image hash before and after recovery and confirmed it was
unchanged. The October 23 screenshot does not establish a fresh whole-image
hash comparison. The recovery tool opens the image read-only.

## Host record and stream

- **Host filename:** `hostfile.txt`
- **Original guest path:** `D:\ADS_Test\hostfile.txt`
- **MFT record:** 58
- **MFT record image offset:** 3,222,333,440 bytes
- **ADS stream:** `CapstoneEvidence`
- **Storage:** Resident, read from the USA-restored MFT record
- **Expected payload length:** 36 bytes
- **Expected SHA-256:**
  `E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E`

Expectations come from the existing
[original ADS payload manifest](../docs/week7_ads_payload_manifest.md), not
from the recovered file itself.

## Recovery procedure and output

Jeff ran this command from the repository root:

```powershell
py code/ntfs_recovery.py "NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd" --record 58 --stream CapstoneEvidence --output "friday_ADS_recovered.bin"
```

The tool selected the named DATA stream, restored the record's sector-tail
bytes in memory, and exported the resident content to a separate new file.
For another run, choose a different output filename; existing outputs are
refused.

- **Recovered filename:** `friday_ADS_recovered.bin`
- **Output path:** Repository root / `friday_ADS_recovered.bin`
- **Actual recovered length:** 36 bytes
- **Actual recovered SHA-256:**
  `E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E`

## Verification results

| Check | Expected | Actual | Result |
|---|---|---|---|
| Host record and stream | Record 58, CapstoneEvidence | Record 58, CapstoneEvidence | PASS |
| Recovered length | 36 bytes | 36 bytes | PASS |
| SHA-256 | Original manifest hash above | Identical recovered hash | PASS |

**Overall result: PASS.** Both the recovered byte count and SHA-256 match
the independent original payload manifest.

## Problems and observations

No recovery error is shown in the captured run. The expected and actual
payload values agree. The result verifies this controlled resident ADS; it
does not establish support for every ADS layout or complete the broader
Milestone 6 test campaign. This original report was prepared from Jeff's
recorded output; Team 3 subsequently completed automated report integration
and a separate real-image run on October 24, documented below.

## Automated integration follow-up — October 24

The same recovery engine now accepts `--report`, `--expected-length`,
`--expected-sha256`, and optional `--expected-image-sha256`. Team 3 ran:

```powershell
py code/ntfs_recovery.py "NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd" --record 58 --stream CapstoneEvidence --output reports/evidence/week10/recovered/team_ads_integrated.bin --report reports/evidence/week10/w10_integrated_ads_report.json --expected-length 36 --expected-sha256 E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E --expected-image-sha256 D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7
```

The [automatically saved report](evidence/week10/w10_integrated_ads_report.json)
records PASS: 36 bytes, matching original payload hash, matching expected
source hash, identical before/after source hashes, and no errors. This is
team integration/testing, not a claim of an individual run by Lucas.
Choose new output/report names to repeat the command; both existing paths
are protected. The full-image hashing takes longer than a normal export.

All **56 regression tests passed** on October 24, including 11 tests for
reporting and CLI failure/safety behavior. See the
[integration test log](evidence/week10/w10_integrated_tests.txt).
Jeff's subsequent run also passed all 56 tests in 1.708 seconds; see the
[updated screenshot](evidence/week10/w10_integrated_tests_summary.png).

## Evidence

- [Jeff's October 23 command and recovery results](evidence/week10/w10_ads_recovery.png)
- [Earlier automated real-image validation](evidence/week10/w10_recovery_validation.json)
- [October 23 regression summary: 45 tests passed](evidence/week10/w10_automated_tests_summary.png)

## Acceptance checklist

- [x] The source image and host record were identified.
- [x] The named ADS stream was selected.
- [x] The payload was recovered to a separate output file.
- [x] The recovered byte count matches the manifest.
- [x] The recovered SHA-256 matches the manifest.
- [x] The report includes the command, actual results, attribution, and evidence.
