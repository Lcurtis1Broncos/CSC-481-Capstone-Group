# Week 9 Parser Validation

**Period:** October 12 - 18, 2026. **Tests performed:** October 15.

## Read-only real-image check

```powershell
python code/ntfs_image_reader.py NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd --show-record 41 --show-record 58
```

| Check | Expected from existing evidence | Observed October 15 | Result |
|---|---|---|---|
| Geometry | 512-byte sectors; 4,096-byte clusters | Same | Pass |
| First MFT record | Absolute offset 3,222,274,048; valid `FILE` | Same | Pass |
| Record 41 | `Testfile.docx`, nonresident, logical 13,437, allocated 16,384 | Same | Pass |
| Run/slack | LCN 3,659, four clusters; slack offset 16,049,277, length 2,947 | Same | Pass |
| Record 58 | `hostfile.txt`; unnamed resident 31 bytes | Same | Pass |
| Controlled ADS | `CapstoneEvidence`, resident 36 bytes | Same | Pass |

The working image was read, not modified. Historical image hashes are in the
manifest; no new whole-image hash was calculated during this check.

Jeff supplied two October 15 screenshots showing the
[command and record 41](../reports/evidence/week9/w9_parser_record41.png)
and the [slack range and record 58 ADS](../reports/evidence/week9/w9_parser_slack_ads.png).
They document the values in the table above.

## Independent manual DATA header check

A separate PowerShell binary read, without importing the Python parser,
read 1,024 bytes at `3,222,274,048 + 58 * 1,024 = 3,222,333,440`.
It checked `FILE`, walked bounded attribute headers, and directly decoded
resident `$DATA` names and content-length fields.

```text
Record 58 absolute offset: 3222333440
Record signature: FILE
Resident DATA: [unnamed] | 31 bytes | attribute offset 312
Resident DATA: CapstoneEvidence | 36 bytes | attribute offset 368
```

These values agree with the parser and Lucas's earlier
[guest-VM stream listing](../reports/evidence/week7/w7_ads_stream_lengths.png).
This checks metadata, not extracted payload contents or recovery hashes.
The reused VM screenshot is historical evidence, not a new Week 9 experiment.

## Automated regression tests

The active suite contains 31 parser/embedding tests. Jeff's October 15
terminal capture shows all 31 tests passing in 0.123 seconds with no skips
or failures.

![Week 9 regression run showing 31 tests and OK.](../reports/evidence/week9/w9_automated_tests.png)

```powershell
python -m unittest discover -s tests -v
```

The original manual ADS workflow and image remain unchanged.

## Independent eight-file size comparison, October 18

Lucas supplied a PowerShell `Get-ChildItem -LiteralPath 'D:\' -File |
Select-Object Name, Length` screenshot from the VM. All eight filenames and
exact byte sizes match the parser's previously recorded unnamed DATA logical
sizes. See the [comparison table](week6_known_file_manifest.md#exact-size-comparison-completed-october-18)
and [source screenshot](../reports/evidence/week9/w9_vm_exact_file_sizes.png).
The Milestone 3 exact-size follow-up is complete. This does not establish
file-content hash equality or recovered-payload validation.

The [design and limitations](parser_design_and_limitations.md) consolidate
the remaining implementation boundaries for Milestone 5.
