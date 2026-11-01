# Week 11 evidence - October 26 to November 1

The [weekly report](../../weekly_report_11.md) embeds the four decisive
screenshots directly, following the professor's October 28 feedback.

| Evidence file | Date/run | What it establishes |
|---|---|---|
| `w11_parser_ads_streams.png` | October 28, Jeff | Record 58's 31-byte unnamed stream and 36-byte named ADS. |
| `w11_ads_recovery_pass.png` | October 29, Jeff | Recovery PASS, original payload match, expected image match, and source unchanged. |
| `w11_ads_recovery_report.json` | October 29, Jeff | Original machine-generated positive recovery report. |
| `w11_ads_expected_hash_fail.png` | October 30, Jeff | Controlled wrong expected hash correctly yields FAIL with matching length and unchanged image. |
| `w11_ads_negative_report.json` | October 30, Jeff | Original machine-generated negative-test report; FAIL is expected. |
| `w11_automated_tests.png` | October 30, Jeff | All 56 tests passed in 1.694 seconds; no skips or failures. |

Screenshots and JSON reports were copied without alteration from Jeff's
provided files. Root-level output paths inside the JSON describe the original
runs; the evidence copies here do not rewrite those paths or execution dates.

The recovered BIN files remain local and are excluded from Git. Both were
independently hashed during documentation preparation; their SHA-256 values
match the actual recovered hash in their respective reports. This small-file
check is not a new full-image hash run. Source before/after hash comparisons
come from the original October 29 and 30 reports.

Lucas's workflow test report/screenshot remain pending; none of these runs
are attributed to him.
