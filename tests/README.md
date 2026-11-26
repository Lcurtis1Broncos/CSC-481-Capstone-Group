# Tests

Run the automated tests from the repository root:

```powershell
py -m unittest discover -s tests -v
```

Tests construct small inputs and check geometry, metadata, resident content,
fragmented data runs, ADS selection, slack boundaries, source preservation,
verification reports, and refusal of invalid or existing destinations.

## Reproducible submission data

```powershell
py tests/generate_submission_dataset.py generated_dataset
py tests/verify_submission.py submission_check
```

Both commands require a new destination folder. The generator writes a
32,768-byte NTFS-shaped fixture, three original payload files, and a manifest
with expected lengths/hashes. It reuses fixture builders in the included test
modules. The verifier generates its own dataset and runs the production CLIs
against it, comparing recovered bytes with those originals. Its JSON summary
records seven acceptance checks, including deliberate failure cases.

These synthetic structures are not a mountable filesystem or the original
Windows lab image. Synthetic expectations remain separate from the
[team-confirmed original-file comparisons](../docs/baseline_hash_verification.md),
recorded November 25 for all eight baseline files. Historical real-image evidence
is retained under `reports/evidence/`; the large images remain outside Git.

Python 3.11 or later is required. On systems without the Windows `py` launcher,
use `python3`. No third-party packages are required.

## Report detection experiment

```powershell
py tests/run_detection_campaign.py detection_campaign_new
```

The report branch adds this 100-image labeled experiment and five tests
(73 tests passed November 25). It measures named-stream screening and a
known-marker search in calculated slack. Optional `--lab-image IMAGE` also
checks the two documented Windows positives and full-image preservation.
The detector does not receive construction labels or planted offsets.
See [results and limitations](../reports/evidence/final_detection/README.md).
Choose a new output folder; no large Windows image is needed for the synthetic run.
