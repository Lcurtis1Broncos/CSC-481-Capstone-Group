# NTFS Slack Space Recovery Workflow

## 1. Preserve the NTFS Evidence Image
- Create a working copy of the original `.dd` image.
- Calculate and record SHA-256 hashes.
- Verify that the working copy matches the original image.

**Evidence Tracking Fields:**
- Evidence ID:
- Original Image Filename:
- Working Image Filename:
- Original Image Size (Bytes):
- Working Image Size (Bytes):
- Original SHA-256 Hash:
- Working Copy SHA-256 Hash:
- Image Creation Date:
- Working Copy Creation Date:
- Analyst Name:

## 2. Identify NTFS Partitions
- Determine the partition offset.
- Identify the sector size.
- Document the NTFS volume boundaries.
- Record the cluster size and filesystem information.

**Evidence Tracking Fields:**
- Evidence ID:
- Image Filename:
- Partition Number:
- Partition Starting Sector:
- Partition Offset (Bytes):
- Partition Size (Bytes):
- Sector Size (Bytes):
- Cluster Size (Bytes):
- NTFS Volume Label:
- Filesystem Type:
- Tool Used:
- Date Examined:

## 3. Identify Files and MFT Records
- Examine the filesystem.
- Identify files that may contain slack space.
- Record relevant MFT record numbers.
- Document file allocation status.

**Evidence Tracking Fields:**
- Evidence ID:
- Original Filename:
- File Path:
- File Extension:
- File Class:
- MFT Record Number:
- Original File Size (Bytes):
- Allocation Status:
- Data Attribute Type:
- Associated Cluster Information:
- Tool Used:
- Date Identified:

## 4. Locate Slack Space
- Determine the allocated clusters associated with each file.
- Identify unused bytes within the final allocated cluster.
- Calculate the expected slack space size.

**Evidence Tracking Fields:**
- Evidence ID:
- Original Filename:
- MFT Record Number:
- File Size (Bytes):
- Cluster Size (Bytes):
- Allocated Cluster Count:
- Final Cluster Number:
- Expected Slack Size (Bytes):
- Slack Space Location:
- Tool Used:
- Date Identified:

## 5. Extract Slack Space
- Use forensic tools to extract slack data.
- Ensure the original evidence image remains unmodified.
- Save extracted data as separate evidence files.
- Record extraction errors or discrepancies.

**Evidence Tracking Fields:**
- Evidence ID:
- Original Filename:
- MFT Record Number:
- Extracted Filename:
- Extraction Method:
- Extraction Tool:
- Tool Version:
- Extracted Byte Length:
- Extraction Date and Time:
- Output File Location:
- Extraction Status:
- Analyst Name:

## 6. Analyze Recovered Data
- Examine extracted bytes for readable text.
- Identify recognizable file signatures.
- Search for recognizable artifacts and test markers.
- Document any recovered content.

**Evidence Tracking Fields:**
- Evidence ID:
- Extracted Filename:
- Recovered Byte Length:
- File Signature Identified:
- Recovered Text:
- Test Marker Identified:
- Artifact Type:
- Hexadecimal Offset:
- Analysis Tool:
- Analysis Findings:
- Date Analyzed:
- Analyst Name:

## 7. Validate and Document Findings
- Calculate SHA-256 hashes of recovered artifacts.
- Record recovered byte lengths.
- Compare recovered data against known test data.
- Create a slack space recovery report documenting findings and discrepancies.
- Preserve recovered artifacts and associated evidence records.

**Evidence Tracking Fields:**
- Evidence ID:
- Original Filename:
- Recovered Filename:
- Original File Size (Bytes):
- Recovered Slack Size (Bytes):
- Recovered Artifact SHA-256:
- Expected SHA-256:
- Hash Match Status:
- Test Marker Match Status:
- Validation Result:
- Discrepancies:
- Recovery Report Location:
- Validation Date:
- Reviewing Analyst:
- Final Evidence Status:

---

## Evidence Handling Requirements

1. Maintain a unique Evidence ID for every recovered artifact.
2. Never modify the original forensic image.
3. Calculate SHA-256 hashes before and after evidence processing where applicable.
4. Preserve original filenames and MFT record references.
5. Record all extraction and analysis timestamps.
6. Document failed recovery attempts and discrepancies.
7. Maintain a chain-of-custody record for collected and transferred evidence.
8. Store recovered artifacts in a controlled evidence directory.

## Final Deliverables

| Deliverable | Description |
|---|---|
| NTFS Evidence Image | Original and working `.dd` images |
| Partition Information | NTFS partition and volume details |
| File Listing | Filenames, sizes, and MFT records |
| Slack Space Extraction | Recovered slack-space data |
| Evidence Tracking Log | Artifact IDs and extraction details |
| Hash Manifest | SHA-256 hashes |
| Analysis Notes | Recovered content and findings |
| Recovery Report | Final validation and discrepancies |
| Chain of Custody | Evidence handling history |
