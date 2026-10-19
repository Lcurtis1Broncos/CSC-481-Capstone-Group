# Evidence Log

| Evidence ID | Date | Description | Source | SHA-256 | Collected / verified by | Storage | Notes |
|---|---|---|---|---|---|---|---|
| E-001 | 2026-09-11 to 2026-09-12 | Earlier full-disk raw baseline image | Dedicated VirtualBox baseline disk | `3815401D2D948B474D1EC104E2C5277ADD1D8DBFAAC4861388319A37EF235814` | Lucas; verified by Jeff | Team transfer link | Hash valid, but BitLocker-protected at the target partition. Not used for NTFS parsing. |
| E-002 | 2026-09-16 | Unencrypted full-disk raw baseline image | Recreated dedicated VirtualBox baseline disk | `EFA4CA3DFA0127F7634EE71D59629A565DCEABB93B23A4A135C5B7AB84AE5E91` | Lucas; independently verified by Jeff | Team transfer link | Clean baseline version, before known files and controlled payloads. |
| E-003 | Week 6, Sept. 21-27 | Eight-file validation image | Lucas's VirtualBox lab export | `053D7CF98D07AAAEE265A1B4D027B384C528ABC55F1D59310B9BFDEE2CB76691` | Lucas supplied hash; no independent download-hash confirmation recorded | Team transfer; image excluded from Git | All eight filenames located; Explorer sizes rounded. |
| E-004 | 2026-10-03 validation | Controlled ADS image | Lucas's VirtualBox lab export | `2240CF8A1AA9D30231C39C4672DC51157093314950C4930EBBF5D30F5F59D2F5` | Lucas; independently verified by Jeff Oct. 3 | Local lab image; excluded from Git | hostfile.txt record 58, CapstoneEvidence resident 36 bytes. |
| E-005 | 2026-10-08 | ADS plus slack working image | New copy made from E-004 by protected embedding tool | `D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7` | Jeff; generated hash and full comparison | Local working image; excluded from Git | Only designated 25-byte marker range changed. Source preserved. |

## Later image and payload records, consolidated October 15

- E-003: `NTFS_Forensic_Baseline_Unencrypted_FilesAdded_RAW.dd`; see the
  [eight-file manifest](week6_known_file_manifest.md) and source screenshot.
- E-004: `NTFS_Forensic_Baseline_ADS_Created_RAW.dd`; see the
  [ADS manifest](week7_ads_payload_manifest.md) for source evidence, marker,
  stream length, and corrected payload hash.
- E-005: `NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd`; see the
  [slack manifest](../reports/evidence/week8/w8_slack_payload_manifest.json)
  for the exact range, payload hash, original bytes, and full comparison.

These entries consolidate earlier results, not new acquisitions or fresh
whole-image hash calculations. No additional ADS image was created October 15;
the original manual ADS experiment remains the controlled source.

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
- **Independent comparison:** Windows `fsutil fsinfo ntfsinfo D:` was run in
  the VirtualBox guest. It matched the parser on the volume serial number,
  bytes per sector, bytes per cluster, file-record size, MFT start LCN, and
  MFT mirror LCN.
- **Findings:** NTFS boot signature valid; 4,096-byte clusters; MFT record 0 at
  byte offset 3,222,274,048; valid `FILE` record signature; volume serial
  number `461C98171C9803D9`.
