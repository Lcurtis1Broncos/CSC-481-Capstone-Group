# Week 7 Attribute-Parser Validation

**Reporting period:** September 28 - October 4, 2026  
**Image used:** `NTFS_Forensic_Baseline_Unencrypted_FilesAdded_RAW.dd`  
**Scope:** Read-only parsing of existing MFT metadata. No bytes in the image
were changed during this validation.

## Parser capability added

The reader now walks the variable-length attributes in an in-use MFT record
and reports these NTFS attribute types:

| Attribute | Type | Information reported |
|---|---:|---|
| `$STANDARD_INFORMATION` | `0x10` | Created time, modified time, and file-attribute flags |
| `$FILE_NAME` | `0x30` | Decoded UTF-16LE file name, logical size, and allocated size |
| `$DATA` | `0x80` | Stream name, logical size, allocated size, and resident/nonresident state |

The file name is displayed in yellow in terminals that support ANSI colors.
Color is a display-only feature; it does not alter parser data or the image.

## Commands used

```powershell
python code\ntfs_image_reader.py "<image path>" --show-record 38
python code\ntfs_image_reader.py "<image path>" --show-record 41
python -m unittest discover -s tests -v
```

To inspect several known records in one run:

```powershell
python code\ntfs_image_reader.py "<image path>" --show-record 38 --show-record 39 --show-record 41 --show-record 42 --show-record 43 --show-record 44 --show-record 55 --show-record 56
```

## Observed results

| MFT record | File | `$DATA` stream | Data state | Logical size |
|---:|---|---|---|---:|
| 38 | `Test.txt` | unnamed | resident | 83 bytes |
| 39 | `Test2.txt` | unnamed | nonresident | 1,778 bytes |
| 41 | `Testfile.docx` | unnamed | nonresident | 13,437 bytes |
| 42 | `SunflowerTest.jpg` | unnamed | nonresident | 48,647 bytes |
| 42 | `SunflowerTest.jpg` | `Zone.Identifier` | resident | 94 bytes |
| 43 | `Thetestfile.pdf` | unnamed | nonresident | 17,247 bytes |
| 44 | `WaterfallTest.png` | unnamed | nonresident | 277,325 bytes |
| 44 | `WaterfallTest.png` | `Zone.Identifier` | resident | 94 bytes |
| 55 | `HTMLtestdoc.html` | unnamed | resident | 608 bytes |
| 56 | `JSON_test_File.json` | unnamed | resident | 579 bytes |

The named `Zone.Identifier` streams are ordinary Windows Mark-of-the-Web
metadata. Their presence demonstrates that the parser recognizes named
`$DATA` streams, but they are not the team's controlled ADS payload and are
not treated as malicious.

## Test result

The automated suite completed successfully with **17 of 17 tests passing**.
The tests cover boot-sector parsing, MBR partition selection, MFT offsets and
records, file-name decoding/listing, `$STANDARD_INFORMATION`, resident and
nonresident `$DATA`, and zero FILETIME formatting.

## Controlled ADS validation on October 3

The supplied `NTFS_Forensic_Baseline_ADS_Created_RAW.dd` image was hashed
locally; its SHA-256 matched Lucas's screenshot. The parser located
`hostfile.txt` in MFT record 58 and reported unnamed resident contents of
31 bytes and a named resident `CapstoneEvidence` stream of 36 bytes. Both
lengths match the source screenshots. See the
[ADS payload manifest](week7_ads_payload_manifest.md) for the full evidence.

## Current limitation

This stage reports metadata only; it does not extract `$DATA` content or
recover a payload. A later recovery test will compare the extracted payload
hash against Lucas's reported SHA-256 value.
