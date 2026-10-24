# Week 10: Data-location and recovery support

**Period:** October 19–25, 2026

**Implementation:** Jeff; October 21

**Milestone:** 6, in progress (October 19–November 8)

## GitHub review

- PR #18 merged Week 9 work on October 18 (`2a9abaa`).
- Lucas added `docs/ADS Recovery Workflow.md` on October 20 (`3f5339d`).
  This supplies the recovery procedure, report fields, acceptance checklist,
  and pass condition. Its blank test fields are not completed recovery results.
- No additional extractor code or tests were present in the reviewed update.
  Jeff confirmed this with Lucas's status as relayed October 21.

## Support functions

`code/ntfs_recovery.py` provides:

- `locate_stream(image, record_number, stream_name="")`: verifies geometry,
  the initialized MFT range, FILE record status, update-sequence fixups,
  stream selection, run coverage, and volume bounds. Returns resident content
  or ordered physical extents plus logical size and the supported slack range.
- `iter_stream_content(location)`: yields bounded chunks in logical order,
  excludes allocation slack, and zero-fills bytes beyond initialized size.
- `recover_stream(location, destination)`: writes a new output only and
  returns actual byte count and SHA-256. Never opens the image for writing.
- `StreamLocation.summary()`: JSON-compatible locations and sizes for the
  extractor/report integration.

Record fixup restoration is now shared in `ntfs_image_reader.py`; the existing
slack embedding tool imports the same function. Its behavior is unchanged.
The parser now exposes initialized size and ending VCN for recovery checks.

## Automated tests

Run from the repository root:

```powershell
py -m unittest discover -s tests -v
```

The October 21 run passed **45 tests**, no skips or failures: the existing
31 tests plus 14 recovery tests. See the saved
[test output](../reports/evidence/week10/w10_automated_tests.txt).
New checks cover sector-tail restoration inside resident content, named-stream
selection, fragmented file runs with a negative LCN delta, EOF truncation,
uninitialized zero-fill, MBR offsets, empty streams, source preservation,
overwrite refusal, and malformed/unsupported records and runs.

The automated agent run used a workspace-local temporary directory because
the tool sandbox restricts its system temporary directory. No execution policy
or machine security setting was changed.

## Independent first-run offset check: three files

The image was opened separately in binary read-only mode. For each record,
the attribute offset and lengths were read with `struct.unpack_from`; the
unnamed DATA mapping pairs were decoded directly with `int.from_bytes`,
without calling `locate_stream`, `decode_data_runs`, or the parser's offset
helpers. These first runs each start at VCN zero, so their first signed LCN
delta is the starting LCN.

| Record/file | Raw first mapping pair plus terminator | First LCN | Clusters | Absolute content offset |
|---|---|---:|---:|---:|
| 39 / Test2.txt | `21 01 74 0e 00` | 3700 | 1 | 16,203,776 |
| 41 / Testfile.docx | `21 04 4b 0e 00` | 3659 | 4 | 16,035,840 |
| 42 / SunflowerTest.jpg | `21 0c 59 0e 00` | 3673 | 12 | 16,093,184 |

Formula: `1,048,576 + LCN × 4,096`. Compare these independently decoded
locations with the extents in the saved real-image report. This is an
independent byte/header calculation, not a comparison with a separate forensic
product. The synthetic tests additionally check exact offsets in constructed
volume-only and MBR images, including fragmented logical content order.

## Real-image recovery check

Input: `NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd`.
The validation runner requires its previously recorded SHA-256 and measures
that hash again after recovery. It exports the eight baseline files and the
known ADS to separate new files. Actual results are saved in
[the validation report](../reports/evidence/week10/w10_recovery_validation.json).

```powershell
py tests/validate_week10_image.py "NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd" --output-directory reports/evidence/week10/recovered --report reports/evidence/week10/w10_recovery_validation.json
```

The saved paths already exist after a successful run. For a rerun, choose a
new output directory (for example `recovered_repeat`) and new report path.
Recovered files are local validation outputs, excluded from Git; the JSON
report is retained. No new disk image or ADS is created.

**Observed October 21:** All eight recovered lengths matched. The ADS length
and original hash matched. The slack range matched. The full image hash was
unchanged before/after:
`D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7`.
The three first-run offsets above also agree with the report's recorded
extents. That manual cross-check was completed separately from the runner;
the runner itself does not perform an independent offset review.

Acceptance checks:

1. Eight names and recovered byte counts match Lucas's VM exact-size evidence.
2. Record 58 `hostfile.txt:CapstoneEvidence` recovers 36 bytes; its SHA-256
   matches the existing manifest:
   `E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E`.
3. Record 41's computed slack matches offset **16,049,277**, length **2,947**.
   This checks the range, not extraction of the slack marker.
4. Before/after source hashes match the recorded working image hash.

Original hashes for the eight baseline files have not been supplied.
Their output hashes are recorded but must not be described as matching original
file hashes. The known ADS has an independent original payload hash.

## Team extractor/report integration — October 24

`recover_with_report` now integrates the existing location/recovery functions
with a new JSON report. This is a Team 3 deliverable built from Lucas's
workflow/report format and the recovery-support engine; it is not a claim
that Lucas independently implemented or ran the integration.

The report includes image path/hash, host filename, record, stream, expected
and actual lengths/hashes, comparison results, source preservation, and
errors. Expectations are supplied from the original manifest, not copied from
the output. Full-image hashes are measured before and after recovery.

`--report` requires `--output`. Use `--expected-length` and
`--expected-sha256` for a verified result. The optional
`--expected-image-sha256` rejects the wrong input image before exporting.
PASS requires both payload comparisons and unchanged image hash. Missing
expectations produce NOT_VERIFIED; mismatches produce FAIL. Both return
nonzero CLI status. A reserved report records ERROR if recovery fails.
Preflight errors do not create a report. Output and report cannot overwrite
existing files or one another or the source image.

Eleven integration tests extend the suite from 45 to **56 passing tests**.
They test the actual CLI as well as API behavior, successful comparisons,
wrong expectations, missing expectations, source changes, malformed inputs,
overwrite/collision prevention, and diagnostic error reporting. See
[October 24 integrated test output](../reports/evidence/week10/w10_integrated_tests.txt).

See the [README command](../README.md#automated-recovery-report) to reproduce
the integrated workflow. Lucas's original blank template remains unchanged;
completed results are saved separately and attributed to their actual runs.

The October 24 real-image integration run passed: 36 recovered bytes and the
original ADS hash matched; source before/after hashes were identical and
matched the supplied expected image hash. The CLI generated
[this report](../reports/evidence/week10/w10_integrated_ads_report.json)
directly, with no manual filling of results.

## Boundaries and remaining evidence

- Only valid in-use ordinary files are supported. No deleted-file recovery,
  directory extraction, GPT, BitLocker decryption, or attribute-list extensions.
- Fragmented **file contents** are supported; fragmented **MFT storage** is
  explicitly refused. The MFT's own DATA run and initialized range are checked
  before computing any selected record offset.
- Compressed, sparse, and encrypted streams are refused, not silently decoded.
- Keep the image unchanged between locating and exporting. The controlled
  validation hashes the whole image before and after its run.
- On failure, a partial output can remain; do not treat it as successful.
- Jeff's personal recovery/test screenshots, both journals, and Friday's
  meeting outcome are now included in the weekly report (updated October 24).
  Team 3's automated report integration is implemented and tested. Lucas's
  original workflow remains credited to him; an independent run by him is
  not claimed. The next phase adds further ADS recovery validation.
- Full ADS testing is scheduled October 26–November 1; slack recovery is
  scheduled November 2–8. The first successful ADS check does not complete
  Milestone 6 by itself.
