# Complete Code Submission

**Verified:** November 24, 2026

**Release tag:** `v1.0-final`

## Assignment requirements

| Requirement | Completion evidence |
|---|---|
| Source code | `code/ntfs_image_reader.py`, `code/ntfs_recovery.py`, and controlled lab tool `code/slack_embed.py`. |
| Test datasets or generation scripts | `tests/generate_submission_dataset.py` builds a deterministic 32 KB fixture and original payloads; no large image download is required. |
| Test thoroughly and address defects | 68 automated tests passed; seven clean-copy acceptance checks passed. Supported boundaries and remaining limitations are documented. |
| Update documents and execution instructions | Root README, source/test READMEs, and parser limitations describe current recovery/reporting behavior and how to reproduce checks. |
| Tagged repository | The verified release commit is identified by `v1.0-final`. |

## Verification performed

Copied the tracked source and new release files into a separate directory
without Git metadata or the local 8 GB lab images. From that copy:

```powershell
py -m unittest discover -s tests -v
py tests/verify_submission.py <new-output-directory>
```

**Results:** 68 tests passed in 8.613 seconds. All seven acceptance checks
passed: metadata/ADS identification; exact fragmented-file, ADS, and slack
recovery; deliberate wrong-hash failure; existing-file protection; and
out-of-range slack refusal. The generated image hash remained unchanged.

The test temporary directory was placed within the writable workspace because
the execution environment restricted its default temporary directory. This
adjustment affects test-file placement, not the test cases or production code.

Saved evidence:

- [Full test output](evidence/final_code/regression.txt)
- [Acceptance summary](evidence/final_code/verification.json)
- [Generated dataset manifest](evidence/final_code/dataset_manifest.json)
- [Parser output](evidence/final_code/parser_output.txt)

## Scope and remaining evidence limitations

This is a release of the supported controlled-image implementation. It does
not support every NTFS feature; fragmented MFT storage, attribute-list
resolution, compressed/encrypted recovery, and automatic hidden-payload
discovery remain outside the implemented scope. The metadata CLI does not
apply record fixups on every path; content recovery validates fixups.

The generated dataset is a handcrafted parser fixture, not a mountable
Windows filesystem. Historical VirtualBox image checks remain separately
documented under weekly evidence. At the November 24 release check, original-file hash comparisons were
pending. On November 25, Jeff confirmed that all eight original-file hashes
match the recorded recovered-file hashes; see the
[dated comparison](../docs/baseline_hash_verification.md). The original release
logs and immutable `v1.0-final` tag retain their dated state.

The final technical report, slides, and presentation are separate deliverables.
The team leader must submit the tagged repository URL to the course site;
creating the GitHub release reference does not perform that submission.
