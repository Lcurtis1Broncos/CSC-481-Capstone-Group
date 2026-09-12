# Evidence Log

| Evidence ID | Date/Time | Description | Source | Hash | Collected by | Location | Notes |
|---|---|---|---|---|---|---|---|
| E-001 | 2026-09-11 to 2026-09-12 | Hash-verified raw baseline disk image | Dedicated VirtualBox baseline disk | SHA-256 recorded below | Lucas Curtis; verified by Jeff Perez | Team file-transfer link; not stored in GitHub | Full-disk image; partition layout requires parser validation |

## E-001 — Baseline raw image

- **Evidence ID:** E-001
- **Date/Time acquired:** September 11-12, 2026
- **Description:** Full raw baseline disk image for controlled parser testing
- **Source:** Dedicated VirtualBox baseline disk
- **Device/media:** 8 GiB virtual disk; MBR partition style
- **File/image name:** `NTFS_Forensic_Baseline_RAW.dd`
- **SHA-256:** `3815401D2D948B474D1EC104E2C5277ADD1D8DBFAAC4861388319A37EF235814`
- **Collected by:** Lucas Curtis
- **Integrity verified by:** Jeff Perez
- **Acquisition method:** VirtualBox medium cloned to RAW format
- **Storage location:** Shared team file-transfer link; hash recorded in repository
- **Access history:** Downloaded and hash-verified by Jeff Perez on September 12, 2026
- **Analysis performed:** Baseline acquisition and integrity verification
- **Findings:** The image is a full-disk image with an MBR at byte offset 0. The
  target partition must be located before NTFS boot-sector fields are parsed.
- **Notes:** The large image file is intentionally not stored in GitHub.
