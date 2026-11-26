# Baseline File Hash Verification

**Current status:** All eight original-file SHA-256 hashes match the recorded recovered-file hashes, as confirmed by Jeff Perez on November 25, 2026.

The recovered hashes and byte counts come from the November 15 recovery
record. The later original-file comparison is a team-reported confirmation,
not a new original-file hashing run by the documentation assistant. Original
command output was not attached to this confirmation. The original values
below are recorded as equal to the recovered values on that stated basis.

| File | MFT record | Recovered bytes | Original and recovered SHA-256 | Comparison |
|---|---:|---:|---|---|
| `Test.txt` | 38 | 83 | `D68EC557336622896727E44ED003136662FCD67CE8F9F57B23E70C0E09ADA797` | Match reported |
| `Test2.txt` | 39 | 1,778 | `BA7F25F70009A6D45A9EF88C857C9C357856AA6D1201486DE9070522CFAEE64E` | Match reported |
| `Testfile.docx` | 41 | 13,437 | `84A8A7AC155C36A5F4F9196A412D8DB16A6F12BD10794FEC362542E562DBE347` | Match reported |
| `SunflowerTest.jpg` | 42 | 48,647 | `658C1F66CE1C2D05B51F4E20044981228AAE39BE33B14737B5ADD448378B9E7C` | Match reported |
| `Thetestfile.pdf` | 43 | 17,247 | `61FCC2B322094257A6B845E15D7AEFF99564E83260EA413DB05180DD8A0E3C8C` | Match reported |
| `WaterfallTest.png` | 44 | 277,325 | `19CE26BC665962B8B6B766C48EFFC8676D1191B7B46CACD165418892ED42AA08` | Match reported |
| `HTMLtestdoc.html` | 55 | 608 | `815246781F0ADE404A0FECD2531CB027AB7F6C1177868967BC7CCA47D88AE0FB` | Match reported |
| `JSON_test_File.json` | 56 | 579 | `65EAF0824C357D4FC9955E75CA29CF3F6476DCB0374241DAB08C3714991E8D34` | Match reported |

The original eight-file content-comparison follow-up is closed on the team's
confirmation. The separate ADS and slack marker checks remain matched.
This update does not change the recorded results of earlier test runs or
imply support for untested NTFS layouts.

Sources:

- [November 15 recovery record](../reports/evidence/week13/image_validation.json).
- [November 25 comparison confirmation](../reports/evidence/final_report/baseline_hash_confirmation.json).

Earlier weekly reports and machine-generated logs retain the status known
when they were written. Their references to unavailable original hashes
describe that earlier evidence state.
