# Evidence Log

| Evidence ID | Date | Description | Source | SHA-256 | Collected / verified by | Storage | Notes |
|---|---|---|---|---|---|---|---|
| E-001 | 2026-09-11 to 2026-09-12 | Earlier full-disk raw baseline image | Dedicated VirtualBox baseline disk | `3815401D2D948B474D1EC104E2C5277ADD1D8DBFAAC4861388319A37EF235814` | Lucas; verified by Jeff | Team transfer link | Hash valid, but BitLocker-protected at the target partition. Not used for NTFS parsing. |
| E-002 | 2026-09-16 | Unencrypted full-disk raw baseline image | Recreated dedicated VirtualBox baseline disk | `EFA4CA3DFA0127F7634EE71D59629A565DCEABB93B23A4A135C5B7AB84AE5E91` | Lucas; independently verified by Jeff | Team transfer link | Current controlled test image. MBR, NTFS boot sector, and MFT record 0 verified. |

## E-001 — Earlier BitLocker-protected baseline image

- **File/image name:** `NTFS_Forensic_Baseline_RAW.dd`
- **Device/media:** 8 GiB virtual disk; MBR partition style
- **Acquisition method:** VirtualBox medium cloned to RAW format
- **Integrity result:** Jeff calculated the same SHA-256 hash provided by Lucas.
- **Analysis performed:** The team inspected the image’s MBR and then read the
  first sector of the target partition at byte offset 1,048,576.
- **Finding:** The partition began with `-FVE-FS-`, which identifies a BitLocker
  volume header rather than an NTFS boot sector.
- **Disposition:** Retained as a documented validation attempt. It is not used
  for the project’s NTFS/MFT, ADS, or slack-space tests.

## E-002 — Validated unencrypted baseline image

- **File/image name:** `NTFS_Forensic_Baseline_Unencrypted_RAW.dd`
- **Source:** Dedicated VirtualBox baseline disk recreated with BitLocker disabled
- **Device/media:** 8 GiB virtual disk; MBR partition style
- **SHA-256:** `EFA4CA3DFA0127F7634EE71D59629A565DCEABB93B23A4A135C5B7AB84AE5E91`
- **Collected by:** Lucas Curtis
- **Integrity verified by:** Jeff Perez on September 16, 2026
- **Acquisition method:** VirtualBox medium cloned to RAW format
- **Storage location:** Shared team file-transfer link; the image itself is not
  stored in GitHub because of its size.
- **Analysis performed:** The parser read the MBR, identified partition 1
  (`0x07`, start LBA 2,048), verified the NTFS boot sector at byte offset
  1,048,576, calculated the absolute `$Mft` offset, and read MFT record 0.
- **Findings:** NTFS boot signature valid; 4,096-byte clusters; MFT record 0 at
  byte offset 3,222,274,048; valid `FILE` record signature; volume serial
  number `461C98171C9803D9`.
