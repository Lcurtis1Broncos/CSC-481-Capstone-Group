# NTFS Recovery Demonstration

Demonstrate how the parser identifies the known ADS and document slack,
then recover both markers and compare their lengths and SHA-256 hashes.
Use the existing Python tools from the VS Code PowerShell terminal.

The confirmed time limit is **8–10 minutes for the entire presentation**.
Target about three minutes for the live demonstration and five to six minutes
for the slides and handoffs. Whole-image hashing is preparation and follow-up
work because the source is about 8 GB.

| Elapsed time | Presenter | Focus |
|---|---|---|
| 0:00–3:00 | Lucas | Problem, lab, and method; highlight the essential slide details. |
| 3:00–6:00 | Jeff | Locate the streams, recover both markers, and show the comparisons. |
| 6:00–8:00 | Lucas | Results, limitations, and conclusion. |
| 8:00–9:00 | Both | Buffer for transitions or a slower command. |

Use the slides as visual support rather than reading every table or hash.

## Before presenting

- Open the repository folder in VS Code and increase the terminal text size
  until commands and results are readable on screen.
- Have Lucas's slides and the report available. Coordinate the handoff after
  his explanation of the lab and the two hiding locations.
- Check that `NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd` is present.
- Run `py -m unittest discover -s tests -v` before the presentation. The release
  suite contains 68 tests. Keep its result available rather than scrolling
  through the entire suite during the demonstration.
- Use a new output directory for every rehearsal. Do not delete or replace
  existing evidence to make a command run again.

Run these commands from the repository root. They set up the paths, create a
new output folder, and verify the expected source-image hash:

```powershell
$demoImage = Join-Path $PWD 'NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd'
$demoOutput = Join-Path $PWD ('demo_output_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $demoOutput | Out-Null
$demoExpectedImageHash = 'D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7'
$demoImageBefore = (Get-FileHash -LiteralPath $demoImage -Algorithm SHA256).Hash
if ($demoImageBefore -ne $demoExpectedImageHash) { throw 'Wrong image or unexpected image change. Stop and check the source.' }
```

Keep this terminal session open so its variables remain available. If the
hash comparison fails, stop rather than changing the expected hash to match
an unexplained image. Avoid other programs writing to the image during the run.

## 1 Explain the two locations

Say:

> Our project examines two places ordinary file viewing can overlook. An ADS
> is a separate named data stream attached to a file. Slack is the unused
> tail of the last cluster containing a nonresident file's content. We placed
> known markers in both locations so we could verify recovery.

## 2 Show the parser output

```powershell
py code/ntfs_image_reader.py $demoImage --show-record 41 --show-record 58
```

Point out these fields rather than reading every line:

| Record | What to show | Meaning |
|---|---|---|
| 41 | `Testfile.docx`, nonresident, logical size 13,437 bytes | The document's normal content is stored in clusters. |
| 41 | Slack offset 16,049,277; length 2,947 bytes | The calculated unused tail after normal content. |
| 58 | `hostfile.txt`, stream `CapstoneEvidence`, resident, 36 bytes | The named hidden payload is inside the MFT record. |

Say:

> The record offset locates metadata. Data-run image offsets locate
> nonresident content. This ADS is resident, so its content comes from the
> validated MFT record. The recovery tool restores the record's sector tails
> before exporting resident bytes.

If the metadata output is too long, use the smaller recovery location views:

```powershell
py code/ntfs_recovery.py $demoImage --record 58 --stream CapstoneEvidence
py code/ntfs_recovery.py $demoImage --record 41 --slack-length 25
```

## 3 Recover the named ADS

```powershell
$demoAds = py code/ntfs_recovery.py $demoImage --record 58 --stream CapstoneEvidence --output (Join-Path $demoOutput 'ads.bin') | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) { throw 'ADS recovery failed.' }
$demoAds | Select-Object host_filename, stream_name, resident, recovered_length, recovered_sha256 | Format-List
$demoAdsMatches = $demoAds.recovered_length -eq 36 -and $demoAds.recovered_sha256 -eq 'E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E'
"ADS length and original hash match: $demoAdsMatches"
```

Expected: **36 bytes**, named stream **CapstoneEvidence**, and **True** for
the comparison. If it prints False, stop and investigate the mismatch.

Say:

> We explicitly selected the named stream. The unnamed host stream contains
> different content. The recovered ADS has the expected length and matches
> the original payload hash recorded in our earlier manifest.

## 4 Recover the slack marker

```powershell
$demoSlack = py code/ntfs_recovery.py $demoImage --record 41 --slack-length 25 --output (Join-Path $demoOutput 'slack.bin') | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) { throw 'Slack recovery failed.' }
$demoSlack | Select-Object host_filename, recovery_kind, host_logical_size, recovered_length, recovered_sha256 | Format-List
$demoSlackMatches = $demoSlack.recovered_length -eq 25 -and $demoSlack.recovered_sha256 -eq '3BF8F582FF237AD7F739D39EDCF54CB35E0E6FDFD75AD47CA55F3598629390F2'
"Slack length and original hash match: $demoSlackMatches"
```

Expected: **25 bytes**, recovery kind **slack_payload**, and **True**.

Say:

> The available slack is 2,947 bytes, but our known marker occupies only 25.
> We recover those 25 bytes instead of exporting the whole unused tail.
> Their hash matches the original slack-payload manifest.

## 5 Explain verification and limitations

Say:

> A payload hash checks the recovered hidden marker. A baseline-file hash
> checks an original ordinary file. An image hash checks the entire disk
> image. We keep those comparisons separate. Matching a filename or length
> alone does not prove that a recovered file matches its original contents.

For the baseline files, say:

> The team confirmed that the original SHA-256 hashes match the recorded
> recovered hashes for all eight ordinary files on November 25. That comparison
> is separate from the two hidden-marker checks.

See the [dated comparison record](../docs/baseline_hash_verification.md).

These quick recovery commands display measured output hashes; the explicit
PowerShell comparisons above check them against the original expectations.
They do not create new integrated verification reports or automatically
hash the complete source before and after each export. The saved historical
JSON reports demonstrate that reporting workflow. Run the final source
check below before claiming preservation for this new demonstration.

Hand back to Lucas for the project conclusion and questions.

## After the demonstration

Check the full source image again in the same terminal:

```powershell
$demoImageAfter = (Get-FileHash -LiteralPath $demoImage -Algorithm SHA256).Hash
$demoSourceUnchanged = $demoImageBefore -eq $demoImageAfter
"Source image unchanged during this demonstration: $demoSourceUnchanged"
if (-not $demoSourceUnchanged) { throw 'Source hash changed. Do not mark the demonstration as verified.' }
```

Keep the two recovered files and capture the comparison results. Mark the
rehearsal complete only after the payload comparisons and source check pass.

## If the large image is unavailable

Use the existing portable acceptance workflow:

```powershell
$demoFallback = Join-Path $PWD ('submission_check_' + [guid]::NewGuid().ToString('N'))
py tests/verify_submission.py $demoFallback
```

Explain that this is the **synthetic 32 KB test fixture**, with different
record numbers and offsets from the Windows lab image. It demonstrates
supported recovery and failure handling but does not replace the original
Windows experiment or verify the eight baseline-file hashes.

## Rehearsal checklist

- [ ] Lucas and Jeff have agreed on the handoff and speaking order.
- [ ] Terminal text and slide text are readable when screen sharing.
- [ ] The correct working-image hash matches before the run.
- [ ] ADS recovery returns 36 bytes and its comparison is True.
- [ ] Slack recovery returns 25 bytes and its comparison is True.
- [ ] The source-image hash matches after the run.
- [ ] The full presentation fits 8–10 minutes, including the approximately
      three-minute demonstration.
- [ ] Both presenters can explain resident content, nonresident content,
      slack, and the three kinds of hashes.
- [ ] Slides use dated test counts and the current eight-file plan.
- [ ] Original-file hash claims agree with the latest recorded comparisons.
- [ ] Slides, report, and saved evidence are accessible for backup.

The speaking rehearsal and actual elapsed time remain to be confirmed by the presenters.
# November 25 detection-results talking point

Slide 12 now reports a separate 100-image experiment. Named-stream screening
found all 25 hidden ADS cases but also flagged ten legitimate named streams:
100% detection and 40% false positives. The slack signature found all 15
plaintext markers and missed ten transformed markers: 60% detection and
40% evasion, with no false positives among 25 controls. Both methods had
80% accuracy on their deliberately balanced 50-case groups.

Explain: "A named stream is a reason to inspect, not proof of concealment.
A literal marker search can miss changed bytes. These rates describe our
constructed test cases, not all Windows files." Keep this to about 30 seconds
within the existing 8–10-minute presentation. No extra live run is necessary.
The latest report-branch suite passed 73 tests; the tagged release passed
68 tests and seven acceptance checks on November 24.
