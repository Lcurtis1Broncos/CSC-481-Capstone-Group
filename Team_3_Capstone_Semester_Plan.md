**SEMESTER PROJECT PLAN**

**NTFS Filesystem Steganography and Forensic MFT Parser**

CSC-481 Capstone Project | Team 3 | August 31-November 29, 2026

| **Team Member**         | **Role and Primary Responsibilities**                                                                                                                   |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lucas Curtis            | Team Leader: NTFS specification study, VirtualBox lab image, tool integration, report structure, evidence coordination, and presentation coordination.  |
| Jeff Perez              | Raw-sector parser lead: boot-sector parsing, MFT location, MFT-entry parsing, \$STANDARD_INFORMATION, \$DATA, parser testing, and technical validation. |
| Shared responsibilities | ADS creation, slack-space embedding, forensic recovery, testing, evidence collection, and the final demonstration.                                      |

**1\. Project Objective**

Develop a controlled NTFS forensic laboratory that demonstrates Alternate Data Stream (ADS) and cluster slack-space data hiding, then uses a Python raw-sector MFT parser and read-only forensic extractor to locate and recover documented test payloads from a .dd disk image.

**2\. Scope and Operating Boundaries**

- All experiments will use a dedicated VirtualBox NTFS image created for this project.
- Tools will use Python binary I/O and documented offsets rather than high-level operating-system file APIs for forensic parsing.
- Writes are limited to copied project test images. No physical disks, production systems, or unauthorized images will be used.
- The recovery tool will operate in read-only mode against the forensic .dd image.

**3\. Success Criteria**

| **Area**          | **Success Criterion**                                                          | **Measurement**                                                                                           |
| ----------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| Lab safety        | All testing occurs on a dedicated VirtualBox image, not a physical drive.      | Evidence log identifies the lab image and confirms no physical drives were used.                          |
| NTFS parsing      | Parser reads required boot-sector and MFT information.                         | Boot-sector values match a trusted NTFS tool; parser lists at least 10 known files.                       |
| Attribute parsing | Parser identifies \$STANDARD_INFORMATION, \$FILE_NAME, and \$DATA information. | Tested records include file name, record number, size, stream name, and data state.                       |
| Data hiding       | ADS and slack-space payloads are embedded in the project image.                | Each payload has a marker, byte length, location record, and SHA-256 hash.                                |
| Forensic recovery | Extractor recovers both hidden payloads from the .dd image.                    | Recovered SHA-256 hashes exactly match the original payload hashes.                                       |
| Evidence          | Results are reproducible and documented.                                       | Evidence log includes image hashes, payload hashes, screenshots, hexdumps, test results, and limitations. |
| Final delivery    | Code and demonstration operate from the repository.                            | Live demonstration runs the parser and shows documented test-artifact recovery.                           |

**4\. Milestones, Ownership, Outputs, and Measures**

**Milestone 1 - Project Setup and Technical Design**

**August 31-September 6**

| **Subtask**                                                                                        | **Owner** | **Output**                                                            | **Measurement**                                                                                                                                     |
| -------------------------------------------------------------------------------------------------- | --------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Research required NTFS on-disk structures; establish repository standards and evidence-log format. | Lucas     | NTFS research notes, repository structure, and evidence-log template. | Notes define at least 8 required structures or fields: boot sector, MFT, \$STANDARD_INFORMATION, \$DATA, ADS, clusters, slack space, and data runs. |
| Design the raw-parser workflow and test approach.                                                  | Jeff      | Parser design document, binary-field map, and initial test checklist. | Design identifies parser inputs, expected outputs, offsets, and validation steps for the boot sector and MFT.                                       |

**Milestone 2 - NTFS Lab Image and Boot-Sector Parser**

**September 7-September 20**

| **Subtask**                                                                                               | **Owner** | **Output**                                                                      | **Measurement**                                                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create the dedicated VirtualBox NTFS disk; export a clean baseline .dd image and record evidence details. | Lucas     | Baseline NTFS image, SHA-256 hash, disk configuration record, and evidence log. | Image opens in the lab; hash is recorded; log lists volume size, partition details, and image-creation date.                                                                             |
| Implement a read-only Python boot-sector parser.                                                          | Jeff      | Boot-sector parser and boot-sector report.                                      | Reports OEM ID, bytes per sector, sectors per cluster, cluster size, MFT and MFT mirror locations, record size, and volume serial number; values match one trusted NTFS inspection tool. |

**Milestone 3 - Initial MFT Parser and File Listing**

**September 21-September 27**

| **Subtask**                                                                      | **Owner** | **Output**                                                    | **Measurement**                                                                                 |
| -------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Prepare a known-file validation set and review parser results against the image. | Lucas     | Validation manifest and parser-review notes.                  | At least 10 known file names and sizes are compared; discrepancies are documented and assigned. |
| Implement MFT location calculation, record reading, and initial file listing.    | Jeff      | Working MFT parser and file inventory in text or JSON format. | Lists at least 10 known files and correctly identifies valid FILE record signatures.            |

**Milestone 4 - Attribute Support and Controlled Hiding**

**September 28-October 11**

| **Subtask**                                                                                                                                    | **Owner** | **Output**                                                                                                 | **Measurement**                                                                                                                                                                                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Build and document the ADS creation workflow using controlled test payloads.                                                                   | Lucas     | ADS creation tool, ADS payload manifest, and working image copy.                                           | At least one ADS payload is created with a unique marker, recorded byte length, host file, stream name, and SHA-256 hash.                                                                                           |
| Extend the parser to read \$STANDARD_INFORMATION, \$FILE_NAME, and \$DATA attributes; implement and document controlled slack-space embedding. | Jeff      | Attribute-parser modules, structured MFT inventory, slack-space embedding procedure, and payload manifest. | Inventory reports filename, record number, file status, stream name, logical size, allocated size, and resident/non-resident state; one slack payload has a marker, byte length, location record, and SHA-256 hash. |

**Milestone 5 - Midterm Integration and Evidence Package**

**October 12-October 18**

| **Subtask**                                                                                | **Owner** | **Output**                                                               | **Measurement**                                                                                                                         |
| ------------------------------------------------------------------------------------------ | --------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Assemble the midterm report package and verify that both hiding techniques are documented. | Lucas     | Midterm report draft, evidence log, hashes, and screenshots or hexdumps. | Package includes lab setup, parser status, ADS evidence, slack-space evidence, hashes, and remaining tasks.                             |
| Verify parser identification of the ADS host file and document parser limitations.         | Jeff      | Midterm parser results, validation notes, and limitations list.          | Parser identifies the ADS host file and stream name; at least one \$DATA result is manually checked using a hex viewer or trusted tool. |

**Milestone 6 - Forensic Recovery and Extractor Implementation**

**October 19-November 8**

| **Subtask**                                                                                                                                     | **Owner** | **Output**                                                                            | **Measurement**                                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Build extractor integration, recovery reports, and ADS recovery workflow.                                                                       | Lucas     | Read-only extractor workflow, recovery report format, and recovered ADS test payload. | ADS payload is recovered from the working .dd image and its SHA-256 hash matches the payload manifest.                                                                                |
| Add parser support to locate file content from \$DATA attributes, including resident data, documented non-resident data runs, and slack ranges. | Jeff      | Data-location and recovery-support functions with test results.                       | Correct disk offsets are calculated for at least 3 test files; supported recovered-content hashes match original files; slack-range calculation identifies the documented test range. |

**Milestone 7 - Full Test Campaign and Forensic Documentation**

**November 9-November 22**

| **Subtask**                                                                         | **Owner** | **Output**                                                                   | **Measurement**                                                                                                        |
| ----------------------------------------------------------------------------------- | --------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Produce forensic evidence materials and finalize the evidence log.                  | Lucas     | Hexdumps, screenshots, image hashes, payload hashes, and final evidence log. | Evidence confirms the location and recovery of both hidden payloads; baseline and working-image hashes are recorded.   |
| Conduct full parser and recovery tests; document pass/fail results and limitations. | Jeff      | Test cases, pass/fail results, parser-output samples, and defect list.       | All planned tests are executed; each failure includes a cause, status, and corrective action or documented limitation. |

**Milestone 8 - Final Report, Slides, Demonstration, and Presentation**

**November 23-November 29**

| **Subtask**                                                                        | **Owner** | **Output**                                                               | **Measurement**                                                                                                                                              |
| ---------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Finalize the technical report, slide deck, project summary, and presentation flow. | Lucas     | Final report, slide deck, project summary, and contribution record.      | Report explains design, methods, findings, limitations, and ethics; slides cover the problem, tools, results, and conclusions.                               |
| Package code and prepare the live parser and recovery demonstration.               | Jeff      | Final code package, updated README, demonstration script, and checklist. | A clean setup runs the parser against the .dd image, reports MFT information, and demonstrates recovery of documented payloads within the presentation time. |

**5\. Weekly Task Ownership**

| **Dates**       | **Lucas**                                                  | **Jeff**                                                                     |
| --------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Aug. 31-Sept. 6 | NTFS research; repository standards; evidence-log template | Parser design; field map; test checklist                                     |
| Sept. 7-13      | Create VirtualBox NTFS lab image                           | Begin boot-sector parser                                                     |
| Sept. 14-20     | Export baseline .dd image; record hashes                   | Validate boot-sector output                                                  |
| Sept. 21-27     | Prepare known-file validation set                          | Implement MFT record reading and file listing                                |
| Sept. 28-Oct. 4 | Create ADS payload workflow                                | Parse \$STANDARD_INFORMATION, \$FILE_NAME, and \$DATA                        |
| Oct. 5-11       | Document ADS workflow and image state                      | Implement slack-space embedding procedure; add named-stream/data-run support |
| Oct. 12-18      | Compile midterm evidence and report draft                  | Validate parser results; document limitations                                |
| Oct. 19-25      | Build extractor integration and recovery-report format     | Implement data-location and recovery-support functions                       |
| Oct. 26-Nov. 1  | Test ADS recovery workflow                                 | Debug and validate ADS recovery using parser output                          |
| Nov. 2-8        | Test slack-space recovery workflow                         | Validate slack-range calculations and recovery results                       |
| Nov. 9-15       | Gather hashes, screenshots, and hexdumps                   | Run test cases; record pass/fail results                                     |
| Nov. 16-22      | Finalize evidence log and technical report                 | Complete regression testing and code documentation                           |
| Nov. 23-28      | Prepare slides; lead rehearsal                             | Package code; update README; prepare live demonstration                      |
| Nov. 29         | Present project results and conclusions                    | Demonstrate parser and recovery workflow                                     |

**6\. Final Presentation and Demonstration**

Final presentation date: November 29, 2026. Lucas will lead the project overview, forensic process, findings, limitations, and conclusions. Jeff will demonstrate the raw-sector parser, MFT output, and recovery workflow. Both members will explain the controlled lab environment, evidence collection process, and the results of ADS and slack-space recovery.

**7\. Required Final Outputs**

- Python raw-sector NTFS parser.
- ADS creation and slack-space embedding tools and procedures.
- Read-only forensic extractor and recovery report.
- Baseline and hidden-data .dd images with recorded hashes.
- Payload and hash manifest.
- Test results, hexdumps, screenshots, and evidence log.
- Final report, slides, README updates, and live demonstration materials.