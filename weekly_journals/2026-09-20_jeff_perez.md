# Weekly Journal - Jeff Perez

**Week:** 5  
**Reporting period:** September 14 - September 20, 2026

## Work completed

- Verified that the team’s replacement baseline image is a full 8 GiB RAW disk
  image and independently calculated a SHA-256 hash matching the value supplied
  by Lucas.
- Used the MBR partition table to identify partition 1 as a `0x07` Windows data
  partition beginning at LBA 2,048, or byte offset 1,048,576.
- Verified that the sector at the partition offset is an NTFS boot sector with
  valid `NTFS` and `55 AA` signatures, 4,096-byte clusters, and MFT start LCN
  786,432.
- Extended the read-only Python parser so it can identify an MBR partition,
  read the NTFS boot sector at the correct offset, and calculate an absolute
  MFT record location in a full-disk image.
- Added three automated tests for the full-disk support and one test for NTFS
  volume-serial decoding. The test suite now has 10 passing tests.
- Ran the updated program on the unencrypted image. It located MFT record 0
  (`$Mft`) at byte offset 3,222,274,048 and validated its `FILE` signature.
- Extended the boot-sector output to report the NTFS volume serial number:
  `461C98171C9803D9`.

## What I learned

An MBR identifies where a partition begins, while an NTFS boot sector explains
how the filesystem inside that partition is organized. The MFT start LCN is a
location relative to the NTFS volume, not necessarily relative to the beginning
of a complete disk image. I learned that a forensic parser must verify each
layer: disk layout, partition, filesystem, and MFT record, rather than assuming a
`.dd` file begins directly with NTFS.

## Problems encountered and resolution

The team’s initial full-disk image was hash-valid but contained a BitLocker
header at the target partition, so direct NTFS parsing was not possible. Lucas
recreated the baseline image with BitLocker disabled. After verifying the new
hash, I confirmed its MBR, NTFS boot sector, and MFT record with the updated
reader.

## Plan for next week

- Parse the first MFT attribute header beginning at byte 56.
- Learn how attribute types, resident data, and non-resident data are stored in
  an MFT record.
- Help create and validate a small known-file set for the controlled image.
