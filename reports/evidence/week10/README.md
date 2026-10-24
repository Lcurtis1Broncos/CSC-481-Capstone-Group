# Week 10 evidence

- `w10_automated_tests.txt`: October 21 regression run, 45 tests passed.
- `w10_recovery_validation.json`: real-image sizes, recovered output hashes,
  ADS manifest comparison, slack range, and source before/after hashes.
- `w10_integrated_tests.txt`: October 24 regression run, 56 tests passed,
  including 11 automated-report integration tests.
- [Jeff's expanded-suite command](w10_integrated_tests_command.png) and
  [final 56-test summary](w10_integrated_tests_summary.png): October 24 rerun,
  56 passed in 1.708 seconds, no failures or skips.
- `w10_integrated_ads_report.json`: October 24 team integration run, generated
  by the recovery command. PASS: 36-byte original payload length/hash matched,
  expected source hash matched, and source before/after hashes were identical.
- `recovered/`: local output files, deliberately excluded from Git.

See [methods and limitations](../../../docs/week10_recovery_support.md).
The [completed ADS recovery report](../../week10_ads_recovery_report.md) maps
Jeff's recorded run into Lucas's recovery-report format.

## Jeff's October 22–23 screenshots

- [Resident recovery, 83 bytes](w10_resident_recovery.png)
- [Nonresident recovery, 13,437 bytes](w10_nonresident_recovery.png)
- [Overwrite refusal](w10_overwrite_refusal.png)
- [Named ADS recovery, 36 bytes and matching hash](w10_ads_recovery.png)
- [Unit-test command and first results](w10_automated_tests_command.png)
- [45 tests passed in 0.297 seconds](w10_automated_tests_summary.png)

The original screenshots were supplied by Jeff and copied without alteration.
The text log records October 21; the screenshots document his later personal
runs. Actual recovered baseline-file hashes still need independent original
hashes before content equality can be claimed.
