# Baseline Image Information

| Evidence detail | Value |
|---|---|
| Disk number | 1 |
| Virtual disk capacity | 8 GiB |
| Partition style | MBR |
| Target partition | Partition 1 (`F:` in the VirtualBox guest) |
| Partition start offset | 1,048,576 bytes |
| Guest volume label | `NTFS_BASELINE` |
| Guest-reported file system | NTFS |
| Raw image file | `NTFS_Forensic_Baseline_RAW.dd` |
| Raw image size | 8,589,930,496 bytes |
| Raw image SHA-256 | `3815401D2D948B474D1EC104E2C5277ADD1D8DBFAAC4861388319A37EF235814` |
| Image preparation date | September 11-12, 2026 |
| Hash verification | Verified independently after download |

## Validation note

The raw image is a full-disk image. Its first sector contains an MBR rather
than an NTFS boot sector, so the parser must locate the target partition before
interpreting NTFS fields. The target partition's precise filesystem layout will
be validated during the next parser test cycle.
