# Controlled ADS Creation Workflow

**Contributor:** Lucas Curtis  
**Source:** `ADS Creation Steps.txt`, supplied by Jeff on October 11, 2026,
and Lucas's Week 7 VM screenshots.  
**Status:** Workflow documented; corrected instructions below have not been
rerun to recreate the existing image.

Lucas manually created the `CapstoneEvidence` named data stream on
`D:\ADS_Test\hostfile.txt` in the dedicated VirtualBox NTFS lab. The parser
identified the host in record 58 and reported the same stream name and length.
This document records that workflow, with corrections supported by the source
screenshots and local command/hash checks. It is not a standalone ADS tool.

## Corrections to the supplied notes

- The executable stream-name assignment correctly says `CapstoneEvidence`;
  the explanatory `CspstoneEvidence` spelling is a typo.
- The notes use `TEAM3`, but the screenshot marker uses `Team3`. Both are
  36 ASCII bytes, but their hashes differ. The screenshot's hash matches
  `CAPSTONE_ADS_TEST_20261001_Team3_001`, so that is the marker below.
- Remove the backslash before `$ADS` in the length-check command.
- `Get-FileHash` has no `-Stream` parameter. Hash the actual ADS bytes with
  a read-only stream instead, consistent with Lucas's screenshot showing
  SHA-256 computed over `$Bytes`.
- The earlier repository transcription of the payload hash contained an
  extra `C`. The correct 64-character SHA-256 is recorded below and in the
  updated ADS manifest. Computing SHA-256 over the exact ASCII marker matches
  the screenshot; this is not an independent extraction from the disk image.

## 1. Create the host file in the controlled VM

Use only the project NTFS lab volume, not a personal or production volume.
The creation commands write files: use a fresh test environment when
reproducing them, not the preserved evidence image. The `ADS_Test` directory
must exist first.

```powershell
$HostFile = "D:\ADS_Test\hostfile.txt"
Set-Content -LiteralPath $HostFile -Value "Controlled ADS test host file" -Encoding ASCII
```

The command writes ordinary unnamed file contents. The captured VM evidence
reports 31 bytes for that unnamed stream; do not infer this length solely
from the text, because the command adds a line ending.

## 2. Create the named stream

```powershell
$StreamName = "CapstoneEvidence"
$Marker = "CAPSTONE_ADS_TEST_20261001_Team3_001"
Set-Content -LiteralPath $HostFile -Stream $StreamName -Value $Marker -NoNewline -Encoding ASCII
```

The stream's path is `D:\ADS_Test\hostfile.txt:CapstoneEvidence`. Writing
the named stream does not replace the host's ordinary unnamed contents.
ASCII plus `-NoNewline` produces the intended 36-byte payload.

## 3. List streams and inspect the marker

```powershell
Get-Item -LiteralPath $HostFile -Stream *
Get-Content -LiteralPath $HostFile -Stream $StreamName
$ADS = Get-Item -LiteralPath $HostFile -Stream $StreamName
$ADS.Length
```

Expected recorded result: unnamed `$DATA` length 31, `CapstoneEvidence`
length 36, and marker `CAPSTONE_ADS_TEST_20261001_Team3_001`.

## 4. Hash the actual stream bytes

This corrected read-only check avoids text decoding/re-encoding and hashes
the bytes in the named stream directly.

```powershell
$AdsReadStream = [System.IO.File]::OpenRead("${HostFile}:$StreamName")
$AdsSha256 = [System.Security.Cryptography.SHA256]::Create()
try {
    "Payload length: " + $AdsReadStream.Length + " bytes"
    $AdsHash = [BitConverter]::ToString($AdsSha256.ComputeHash($AdsReadStream)).Replace("-", "")
    "SHA-256: " + $AdsHash
} finally {
    $AdsReadStream.Dispose()
    $AdsSha256.Dispose()
}
```

Expected SHA-256 from Lucas's screenshot and exact-marker verification:

```text
E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E
```

## 5. Export and validate the image

Lucas exported the VM lab disk to
`NTFS_Forensic_Baseline_ADS_Created_RAW.dd` using VirtualBox RAW conversion
and recorded its image SHA-256. Jeff independently matched that image hash
and inspected MFT record 58. The parser reported a resident 36-byte
`CapstoneEvidence` stream, matching the VM evidence.

See the [ADS payload manifest](week7_ads_payload_manifest.md) for the image
hash and [Week 7 report](../reports/weekly_report_07.md) for the parser and
source screenshots. Future read-only extraction must compare the recovered
ADS bytes with the payload hash above; metadata agreement alone is not
payload recovery.
