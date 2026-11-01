Test Information

- Test ID: 001
- Date: 11/1/2026
- Person Running the Test: Lucas Curtis
- Recovery Tool / Parser Version:
- Test Status: Pass

Source Image

- Source Image Name: NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd
- Source Image Path: Repository root, supplied as the filename above
- Source Image SHA-256: D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7

Host Record and Stream

- Host Filename: hostfile.txt
- MFT Record Number: 58
- ADS Stream Name: CapstoneEvidence
- Expected Payload Length (bytes): 36 bytes
- Expected Payload SHA-256: E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E
 
Recovery Output

- Actual Recovered Length (bytes): 36 bytes
- Actual Recovered SHA-256: E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E

Verification Results

- Byte Count Match: Pass
- SHA-256 Match: Pass
- Overall Result: Pass

Problems and Observations

- Errors Encountered: 0
- Discrepancies: 0
- Notes: Everything passed; output matches the expected values. 

Recovery Procedure

1. Select the working .dd image and record its SHA-256 hash.
2. Identify the host file's MFT record and named ADS stream using the
   parser.
3. Choose a new output filename in the recovery output directory.
4. Run the integrated recovery command.
5. Record the recovered byte count and SHA-256 hash.
6. Compare the recovered values with the original payload manifest.
7. Document the result and any errors.
