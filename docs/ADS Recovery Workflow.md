Test Information

- Test ID:
- Date:
- Person Running the Test:
- Recovery Tool / Parser Version:
- Test Status:

Source Image

- Source Image Name:
- Source Image Path:
- Source Image SHA-256:

Host Record and Stream

- Host Filename:
- MFT Record Number:
- ADS Stream Name:
- Expected Payload Length (bytes):
- Expected Payload SHA-256:

Recovery Output

- Recovered Output Filename:
- Recovered Output Path:
- Actual Recovered Length (bytes):
- Actual Recovered SHA-256:

Verification Results

- Byte Count Match:
- SHA-256 Match:
- Overall Result:

Problems and Observations

- Errors Encountered:
- Discrepancies:
- Notes:

Recovery Procedure

1. Select the working .dd image and record its SHA-256 hash.
2. Identify the host file's MFT record and named ADS stream using the
   parser.
3. Choose a new output filename in the recovery output directory.
4. Run the integrated recovery command when available.
5. Record the recovered byte count and SHA-256 hash.
6. Compare the recovered values with the original payload manifest.
7. Document the result and any errors.

Acceptance Criteria

- [ ] The correct source image and host record were identified.
- [ ] The correct named ADS stream was selected.
- [ ] The payload was recovered to a separate output file.
- [ ] The recovered byte count matches the manifest.
- [ ] The recovered SHA-256 hash matches the manifest.
- [ ] The recovery report is complete and reproducible.

Pass Condition: The recovered byte count and SHA-256 hash both match the original payload manifest.
