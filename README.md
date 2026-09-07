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

This project is developing a Python-based NTFS forensic parser. The current
tool reads the boot sector of a controlled `.dd` disk image and reports basic
NTFS information, including cluster size and the Master File Table (MFT)
location.

## Installation

1. Install Git and Python 3.9 or later.
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
