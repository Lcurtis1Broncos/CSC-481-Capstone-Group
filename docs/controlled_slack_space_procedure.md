# Controlled Slack-Space Embedding Procedure

## Purpose and scope

This procedure documents a controlled experiment for the dedicated
VirtualBox NTFS lab volume. It must never be
used on a physical drive or unapproved media.

Slack space is the unused portion of the final allocated cluster of a
nonresident file. For example, a file with a logical size of 5,000 bytes on a
4,096-byte-cluster volume occupies two clusters (8,192 bytes), leaving up to
3,192 bytes after the logical end of the file. That unused tail is slack.

## Safety requirements

- Use only a disposable, unencrypted copy of the team VirtualBox NTFS image.
- Shut down the guest before exporting or inspecting the resulting RAW image.
- Never run the embedding method on a physical disk, mounted evidence image,
  or the team's clean baseline image.
- Record the input image hash before the experiment and the working-image hash
  after it.
- Use a short, unique text marker and record its exact byte length and
  SHA-256 hash before embedding.

## Implemented procedure

1. Use the verified ADS lab image as a read-only source. The embedding tool
   creates a new working image and refuses to overwrite an existing file.
2. Select an existing nonresident host file. Record
   its file name, logical size, allocated size, MFT record number, and the
   relevant `$DATA` run information.
3. Prepare a small controlled payload with a unique marker. Record the marker,
   byte length, SHA-256 hash, host file, and intended byte range.
4. Run `code/slack_embed.py` to locate the final-cluster tail using the file's
   data runs and logical size, copy the RAW image, verify the known source
   hash, and write the marker within that tail on the copy.
5. The tool compares every output byte with the source plus the designated
   marker range and calculates the working-image SHA-256. It also records
   the bytes replaced within slack. File contents and metadata are preserved.
6. Validate the host-file metadata and calculated slack range with the parser.
7. Save the generated manifest. Later recovery tests will locate and read the
   documented range independently and compare the recovered payload hash.

## Command for the controlled image

Run from the repository root, using new destination and manifest paths:

```powershell
python code/slack_embed.py NTFS_Forensic_Baseline_ADS_Created_RAW.dd NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd --record 41 --marker TEAM3_SLACK_TEST_20261008 --manifest reports/evidence/week8/w8_slack_payload_manifest.json
```

The tool accepts only the previously verified ADS lab image's SHA-256. It
requires an ordinary nonresident stream with complete data runs and refuses
resident, compressed, sparse, encrypted, and extension-record cases. A failed
operation may leave a partial copy for inspection; it never modifies the source.

To review the location without changing the image:

```powershell
python code/ntfs_image_reader.py NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd --show-record 41
```

## Required evidence

| Item | Required record |
|---|---|
| Baseline and working images | File names, SHA-256 hashes, and storage locations |
| Host file | Path, MFT record number, logical size, allocated size, and data runs |
| Payload | Unique marker, byte length, and SHA-256 hash |
| Slack calculation | Cluster size, logical end, allocated end, and calculated slack range |
| Validation | Parser output, hexdump or trusted-tool comparison, and screenshots |
| Recovery | Recovered bytes, SHA-256 comparison, result, and limitations |

## Status

The embedding tool and data-run/slack calculations are implemented and covered
by automated tests. The generated manifest records the outcome of each real
embedding run. This is a controlled embedding experiment; generalized forensic
content recovery remains a later project phase.
