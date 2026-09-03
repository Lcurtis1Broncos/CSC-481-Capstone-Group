# Weekly Journal - Jeff Perez

**Week:** 3  
**Reporting period:** August 31 - September 6, 2026

## Work completed

- Completed introductory research on how NTFS organizes data: sectors,
  clusters, the Master File Table (MFT), file attributes, Alternate Data
  Streams (ADS), and file slack.
- Created the first Python component for the project: an NTFS disk-image
  reader that opens a `.dd` image in read-only mode, displays the first 512
  bytes, and extracts basic NTFS boot-sector information.
- Tested the reader with the controlled `7-ntfs-undel.dd` practice image. The
  program correctly identified NTFS, a 1,024-byte cluster size, the MFT start
  logical cluster number, and a valid boot-sector signature.
- Added automated tests for two valid NTFS cluster layouts and for safely
  rejecting an image that is shorter than one sector. I also checked that the
  program warns when a selected file is not an NTFS boot sector.
- Submitted the code and tests for team-leader review in pull request #7.

## What I learned

- A sector is a small unit of disk storage, while a cluster is the unit NTFS
  allocates to a file. A file can have unused bytes in its final allocated
  cluster; those bytes are called file slack.
- The MFT is similar to a card catalog for NTFS. It stores records that help
  the operating system locate files and their attributes.
- ADS is a legitimate NTFS feature that can store extra named data attached to
  a file. It can hold normal metadata, but it can also be relevant forensic
  evidence when viewed with other context.
- A `.dd` image is a bit-for-bit copy used for forensic analysis. The NTFS
  boot sector gives the parser the sector size, cluster size, and the MFT
  location needed for later analysis.
- Building a forensic parser is more manageable when it is split into small,
  testable steps instead of attempting the whole tool at once.

## Problems encountered

- I am new to Python and NTFS internals, so it was initially difficult to
  connect the terminology to the code. Breaking the work into short lessons
  and validating each result against a controlled practice image helped.
- The boot-sector reader begins by reading 512 bytes because the image must be
  read before the program can learn the image's own sector and cluster values.
  The program now uses those values for its later calculations.
- The team is working with two members after the third member dropped the
  course, so we need to communicate clearly and keep our tasks focused.

## Plan for next week

- Extend the reader to use the boot-sector information to locate and read the
  first MFT record.
- Learn the structure of an MFT record and begin identifying common
  attributes such as `$STANDARD_INFORMATION`, `$FILE_NAME`, and `$DATA`.
- Continue using controlled NTFS images for testing and coordinate results
  with Lucas as the team leader.
- Review team feedback on pull request #7 and make any requested corrections.
