# Week 7 ADS Payload Manifest

**Source:** Lucas Curtis's VirtualBox screenshots and supplied RAW image.  
**Parser validation date:** October 3, 2026

| Field | Value |
|---|---|
| Guest host-file path | `D:\ADS_Test\hostfile.txt` |
| Stream name | `CapstoneEvidence` |
| Payload marker | `CAPSTONE_ADS_TEST_20261001_Team3_001` |
| Payload length | 36 bytes |
| Payload SHA-256 (reported by Lucas) | `E3CB29B996899849E804A8FD7DB33F7CCECCBCB2569005353BD082D320D0D997E` |
| Normal unnamed stream length | 31 bytes |
| RAW image | `NTFS_Forensic_Baseline_ADS_Created_RAW.dd` |
| Image length | 8,589,930,496 bytes |
| Image SHA-256 | `2240CF8A1AA9D30231C39C4672DC51157093314950C4930EBBF5D30F5F59D2F5` |
| Image integrity check | Independently calculated locally on October 3; matches Lucas's screenshot |
| Host-file MFT record | 58 |
| Parsed ADS state | Resident, 36 bytes |

## Validation

The file listing located `ADS_Test` in record 57 and `hostfile.txt` in record
58. The selected-record summary reported two resident `$DATA` attributes:
the unnamed normal contents (31 bytes) and `CapstoneEvidence` (36 bytes).
The names and lengths match Lucas's guest-VM evidence.

```powershell
python code\ntfs_image_reader.py NTFS_Forensic_Baseline_ADS_Created_RAW.dd --show-record 58
```

The stream name differs from the earlier suggested `project_note`; the
manifest records the actual name created by Lucas. Payload recovery and an
independent recovered-payload hash comparison remain future work. The payload
hash above is Lucas's reported value, while the image hash was independently
verified here.

## Source screenshots

- [Host file, stream, marker, length, and payload hash](../reports/evidence/week7/w7_ads_stream_info.png)
- [Payload hash in the guest VM](../reports/evidence/week7/w7_ads_payload_hash.png)
- [RAW export and image hash](../reports/evidence/week7/w7_ads_image_hash.png)
- [Normal and named stream lengths](../reports/evidence/week7/w7_ads_stream_lengths.png)
