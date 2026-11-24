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
Windows lab image. Synthetic expected hashes do not replace the missing
original hashes for the eight baseline files. Historical real-image evidence
is retained under `reports/evidence/`; the large images remain outside Git.

Python 3.11 or later is required. On systems without the Windows `py` launcher,
use `python3`. No third-party packages are required.
