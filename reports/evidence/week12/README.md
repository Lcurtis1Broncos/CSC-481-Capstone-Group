# Week 12 evidence

- `w12_slack_location.png`: Jeff's November 3 record 41 location output.
- `w12_manual_marker_recovery.png`: Jeff's November 4 read-only manual
  extraction; 25 bytes displaying the expected marker.
- `w12_automated_tests.txt`: November 6 agent-run suite, 64 tests passed in
  2.656 seconds. Includes eight new bounded-slack recovery tests.
- `w12_automated_tests_command.png` and `w12_automated_tests_summary.png`:
  Jeff's November 6 rerun, 64 tests passed in 4.741 seconds, no failures or skips.
- `w12_slack_recovery_report.json`: integrated real-image run, including
  expected/actual payload values and complete source before/after hashes.
- `w12_slack_recovery_pass.png`: Jeff's display of the saved November 6
  integrated report; shows 25-byte hash match, source unchanged, and PASS.
- `recovered/`: local recovered output files, excluded from Git.

The original payload expectations are in the
[Week 8 manifest](../week8/w8_slack_payload_manifest.json). Source images and
manifests were not modified. Provided screenshots were copied without editing.
The integrated result and expanded-suite screenshots are embedded directly
in the weekly report. Displaying the saved report is not a new recovery run.
