# Weekly Journal - Jeff Perez

**Week:** 4  
**Reporting period:** September 7 - September 13, 2026

## Work completed

- Extended our read-only NTFS image reader so it finds and reads the first Master File Table (MFT) record, record 0 (`$Mft`).
- Used the boot-sector values already parsed by the program to calculate the MFT record location: MFT start LCN × bytes per cluster.
- Added validation for the `FILE` record signature and displayed useful header details: record number, byte offset, record size, first attribute offset, in-use status, and directory status.
- Ran the program against the controlled NTFS disk image. It found `$Mft` at byte offset 2,053,120 and confirmed that the record has a valid `FILE` signature.
- Added three tests for the MFT-reader work. The full automated test suite now has six passing tests.

## What I learned

The MFT is the NTFS volume's catalog of file and directory records. The boot sector provides the MFT start location as an LCN (logical cluster number), and the reader converts that value into a byte offset using the cluster size. The bytes `46 49 4C 45`, displayed as `FILE`, identify an MFT record header; they are not the beginning of every ordinary file's contents. Record 0 is the special `$Mft` record that describes the MFT itself.

## Problems encountered

At first, I mixed up an MFT record's `FILE` signature with a normal file signature. Testing the reader on the controlled image helped clarify the difference: the boot-sector location leads to the MFT record, and the `FILE` value validates that record header. I also practiced running both the program and its tests from the VS Code terminal.

## Plan for next week

- Review the Week 4 MFT-reader result and evidence with Lucas during the team wrap-up meeting.
- Continue building the parser carefully, beginning with MFT attributes and file-record details.
- Add the Week 4 test screenshots and both team members' completed work to the weekly team report.
