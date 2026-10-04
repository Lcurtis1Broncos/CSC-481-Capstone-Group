# Controlled Slack-Space Embedding Procedure

## Purpose and scope

This procedure documents a future controlled experiment for the dedicated
VirtualBox NTFS lab volume. It is not a recovery procedure and must never be
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

## Planned procedure

1. Create a working copy of the dedicated NTFS lab image and label it as the
   slack-space test image.
2. Create a host file large enough to require at least two clusters. Record
   its file name, logical size, allocated size, MFT record number, and the
   relevant `$DATA` run information.
3. Prepare a small controlled payload with a unique marker. Record the marker,
   byte length, SHA-256 hash, host file, and intended byte range.
4. Use a documented, repeatable lab-only method to write only within the host
   file's final allocated-cluster tail, after its logical end and before the
   allocated end. The exact method and command will be added after team review.
5. Export the powered-off working image as RAW and calculate its SHA-256 hash.
6. Validate the host-file metadata and calculated slack range with the parser.
7. In a later recovery phase, read the documented slack range from the RAW
   image, extract the expected payload length, and compare the recovered
   SHA-256 hash to the manifest.

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

This is a controlled procedure draft only. No slack payload has been embedded,
and no recovery claim is being made at this stage.
