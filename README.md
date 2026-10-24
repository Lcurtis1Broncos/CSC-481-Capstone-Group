# CSC-481 Capstone — Team 3

## Team Repository for Our Capstone Project

We are a two-person CSC-481 capstone team working together to complete our
project. This repository will organize our application source code,
documentation, meeting minutes, testing materials, presentations, and other
project deliverables.

## Our Goal

Our goal is to learn how to work effectively as a team by collaborating,
relying on each other's strengths and experiences, and delivering a project
that meets our professor's expectations.

## Project Overview

This project is developing a Python-based NTFS forensic parser and read-only
recovery tool. It reports boot geometry, MFT metadata, and supported content
locations, recovers ordinary file streams, and can save verification reports
for controlled `.dd` images.

## Installation

1. Install Git and Python 3.11 or later.
2. Clone the repository and open its folder:

   ```powershell
   git clone https://github.com/Lcurtis1Broncos/CSC-481-Capstone-Group.git
   cd CSC-481-Capstone-Group
   ```

No external Python packages are required at this stage.

## Run the Current Tool

From the repository root, run the NTFS image reader with a controlled `.dd`
image:

```powershell
python code/ntfs_image_reader.py "path\to\image.dd"
```

The reader opens the image in read-only mode and displays basic NTFS
boot-sector information.

## Run Tests

From the repository root, run:

```powershell
python -m unittest discover -s tests -v
```

## Locate and Recover File Content

The recovery support layer reads ordinary resident and nonresident streams
from the controlled NTFS image. Locate first, without writing output:

```powershell
py code/ntfs_recovery.py "NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd" --record 41
```

Recover the known ADS to a **new** separate file:

```powershell
py code/ntfs_recovery.py "NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd" --record 58 --stream CapstoneEvidence --output "recovered_ads.bin"
```

The JSON result reports the recovered length and SHA-256. Compare both with
the payload manifest; an output hash alone does not establish a match.
Existing outputs are refused. Input images are never opened for writing.
See [Week 10 recovery support](docs/week10_recovery_support.md) for validation,
supported boundaries, and the team reporting workflow.

### Automated recovery report

Add `--report`, `--expected-length`, and `--expected-sha256` to generate a new
JSON report using the original manifest's expectations:

```powershell
py code/ntfs_recovery.py "NTFS_Forensic_Baseline_ADS_Slack_Working_RAW.dd" --record 58 --stream CapstoneEvidence --output "ads_verified.bin" --report "ads_verified_report.json" --expected-length 36 --expected-sha256 E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E --expected-image-sha256 D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7
```

This hashes the entire source image before and after recovery, so it takes
longer than a location-only command. Image, output, and report must be
distinct; output/report paths must be new and their parent folders must exist.
The optional expected image hash refuses recovery from the wrong image.

- `PASS`: payload length and hash both match, and source hash is unchanged.
- `FAIL`: a payload expectation differs or the source hash changed.
- `NOT_VERIFIED`: a required original payload expectation was omitted.
- `ERROR`: recovery failed after reserving the report; inspect its error list.

CLI exit status is 0 for PASS, 1 for FAIL/NOT_VERIFIED, and 2 for input or
recovery errors. Preflight errors create no output/report. Failures after
reservation may leave a diagnostic report or partial output; do not label
these successful recoveries. Existing files are never automatically replaced.

## Safety Note

Use only controlled practice images or images you are authorized to examine.
Do not test the parser on another person's device or data without permission.

## Team Members

### Lucas Curtis — Team Leader

I am graduating this semester with a bachelor’s degree in Cybersecurity. 
In the future, I would like to work in the field of digital forensics, 
where I can use my cybersecurity knowledge to investigate and analyze digital evidence. 
I look forward to gaining more hands-on experience through this project, especially learning 
how to communicate, cooperate, and work effectively as part of a group. I hope this experience 
will help me develop skills that I can carry into my future career.

### Jeff Perez — Team Member

I am completing my bachelor's degree in Cybersecurity and hope to pursue a
career in information technology with the United States Postal Service, where I
currently work as a Sales, Services, and Distribution Associate. I am a husband
and father of three, and in my free time I enjoy early-morning runs around Fort
Bragg while training for the Marine Corps Marathon and New York City Marathon
in 2027. During my final two semesters, I plan to learn as much as possible to
prepare for future opportunities in IT and cybersecurity.
