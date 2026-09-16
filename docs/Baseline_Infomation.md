# Baseline Image Information

## Current validated test image

| Evidence detail | Value |
|---|---|
| Disk number | 1 |
| Virtual disk capacity | 8 GiB |
| Partition style | MBR |
| Target partition | Partition 1 (`F:` in the VirtualBox guest) |
| Partition type | `0x07` (Windows data partition) |
| Partition start LBA | 2,048 |
| Partition start offset | 1,048,576 bytes |
| Guest volume label | `NTFS_BASELINE` |
| File system verified by parser | NTFS |
| Raw image file | `NTFS_Forensic_Baseline_Unencrypted_RAW.dd` |
| Raw image size | 8,589,930,496 bytes |
| Raw image SHA-256 | `EFA4CA3DFA0127F7634EE71D59629A565DCEABB93B23A4A135C5B7AB84AE5E91` |
| Team verification date | September 16, 2026 |
| Hash verification | Lucas supplied the hash; Jeff independently calculated a matching SHA-256 hash after download |

## Parser validation results

The image is a full-disk image. Its first sector is an MBR, so the parser
locates partition 1 before interpreting NTFS fields. The updated reader
verified the NTFS boot sector and successfully read MFT record 0 (`$Mft`).

| Parser result | Value |
|---|---:|
| NTFS bytes per sector | 512 |
| Sectors per cluster | 8 |
| Bytes per cluster | 4,096 |
| MFT start LCN | 786,432 |
| Absolute MFT record 0 offset | 3,222,274,048 bytes |
| MFT record signature | `FILE` (valid) |
| NTFS volume serial number | `461C98171C9803D9` |

## Earlier image and remediation

An earlier full-disk raw image had SHA-256
`3815401D2D948B474D1EC104E2C5277ADD1D8DBFAAC4861388319A37EF235814`.
The team verified its hash but found a BitLocker (`-FVE-FS-`) header at the
target partition offset. It is retained only as a record of the validation
attempt; it is not the image used for NTFS/MFT parser testing. Lucas recreated
the baseline with BitLocker disabled and exported the validated unencrypted
image listed above.
