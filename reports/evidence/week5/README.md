# Week 5 Evidence

This folder contains the genuine VS Code terminal screenshots supporting the
Week 5 tests. Each screenshot includes the relevant command and final result.

| File name | Required visible evidence |
|---|---|
| `w5_ntfs_partition_identifier.png` | Manual PowerShell check reading the sector at byte offset 1,048,576 and showing the `NTFS` identifier. |
| `w5_ntfs_boot_sector_fields.png` | Manual PowerShell check showing 512-byte sectors, 8 sectors per cluster, 4,096-byte clusters, MFT start LCN 786,432, and a valid boot signature. |
| `w5_full_disk_mft_reader.png` | The `python code/ntfs_image_reader.py ...Unencrypted_RAW.dd` command and the MBR partition summary, valid NTFS boot-sector summary, and valid `FILE` MFT record result. |
| `w5_automated_tests.png` | The `python -m unittest discover -s tests -v` command and all 10 tests passing. |

All four listed Week 5 screenshots have been added.
