# Parser Design and Limitations

**As-built documentation:** October 15, 2026. This consolidates the existing
implementation; it is not a claim that a standalone design document existed
at the start of the semester.

## Inputs, processing, and outputs

The read-only Python reader accepts a controlled RAW `.dd` image. For the
lab's MBR full-disk image, it selects a `0x07` partition and verifies the NTFS
boot-sector identifier. A volume-only input can begin directly at the boot
sector. Output is terminal text: boot geometry, record headers, a bounded
filename listing, selected attribute summaries, and supported data-run/slack
locations. As of October 21, the separate `ntfs_recovery.py` support layer can
locate and export supported file streams; see the Week 10 validation below.

Processing follows this sequence:

1. Read the first sector; locate the NTFS volume if an MBR is present.
2. Decode geometry and calculate the first MFT record's absolute byte offset.
3. Read the selected fixed-size records and inspect `FILE` headers/flags.
4. Walk attributes and decode standard information, filenames, and data metadata.
5. Decode nonresident mapping pairs and calculate supported content/slack offsets.

## Field map used by the implementation

Offsets below are relative to the indicated structure, not the entire image.
Multi-byte integer fields are little-endian unless identified as text.

| Structure | Offset | Interpretation |
|---|---|---|
| MBR | `0x1BE` | Four 16-byte partition entries; type at entry +4, start LBA at +8. |
| NTFS boot sector | `0x03`, 8 bytes | OEM identifier `NTFS    `. |
| NTFS boot sector | `0x0B`, 2 bytes; `0x0D`, 1 byte | Bytes per sector; sectors per cluster. |
| NTFS boot sector | `0x28`, 8 bytes | Total sectors. |
| NTFS boot sector | `0x30`, `0x38`, 8 bytes each | MFT and MFT mirror LCNs. |
| NTFS boot sector | `0x40`, signed byte | Record-size encoding: negative value means a power of two. |
| NTFS boot sector | `0x48`, 8 bytes; `0x1FE`, 2 bytes | Volume serial; `55 AA` signature. |
| MFT record | `0x00`, 4 bytes | `FILE` signature. |
| MFT record | `0x14`, 2 bytes; `0x16`, 2 bytes | First-attribute offset; record flags. |
| Attribute | `0x00`, `0x04`, 4 bytes each | Type; total attribute length. |
| Attribute | `0x08`, `0x09`, 1 byte each; `0x0A`, 2 bytes | Nonresident flag; name character count; name offset. |
| Resident attribute | `0x10`, 4 bytes; `0x14`, 2 bytes | Content length; content offset. |
| Nonresident attribute | `0x10`, 8 bytes; `0x20`, 2 bytes | Starting VCN; mapping-pairs offset. |
| Nonresident attribute | `0x28`, `0x30`, `0x38`, 8 bytes each | Allocated, logical, and initialized size. |

For this lab, partition offset is 1,048,576, cluster size is 4,096, and the
first MFT record is at 3,222,274,048. File content location is
`partition offset + LCN * cluster size`. Record selection currently uses
`first MFT offset + record number * record size`, assuming contiguous MFT storage.

## Safety and supported boundaries

- The reader opens input images in binary read-only mode.
- `slack_embed.py` is a separate write-capable lab tool. It verifies its known
  source, creates a new destination, validates record fixups, and compares the
  complete output against the source plus the intended marker range.
- General fragmented-MFT traversal and extension-record/attribute-list
  resolution are not implemented. A successful lab run is not universal NTFS support.
- The recovery layer applies the shared sector-tail fixup checks before
  reading attributes or resident contents. The original metadata-reader CLI
  does not yet apply those checks in every parsing path; its output is not a
  substitute for the recovery layer's validated content.
- Sparse runs can be recognized, but slack embedding excludes sparse,
  compressed, encrypted, resident, and extension-record streams.
- Filename metadata is not the same as recovered contents. Use `$DATA` for
  current stream sizes; `$FILE_NAME` size fields can differ.
- Bounded scans can omit records beyond the requested limit. Unsupported or
  malformed records skipped by listing must not be interpreted as absent files.
- GPT, BitLocker decryption, complete path reconstruction, and automatic
  hidden-payload discovery are not demonstrated by this implementation.

## Validation checklist

The tests cover valid and malformed sectors/records, filename and attribute
decoding, signed data runs, sparse runs, slack boundaries, and protected image
copying. Independent Windows output and manual byte reads complement unit
tests. See [Week 9 validation](week9_validation.md) for the latest results.
The [Week 10 recovery-support record](week10_recovery_support.md) describes
the new support functions, independent first-run checks for three files, and
the first recovered ADS hash comparison. Original hashes for the eight baseline
files remain needed for independent content verification. These checks do not
complete the full ADS/slack recovery campaign scheduled through November 8.
