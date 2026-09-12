# Weekly Journal - Lucas Curtis

**Week:** 4  
**Reporting period:** September 7 - September 13, 2026

## Work completed

- Created a dedicated VirtualBox baseline disk for the project.
- Recorded the disk configuration and initial evidence details.
- Created and shared a full raw disk image for team testing, then recorded its
  SHA-256 hash.

## What I learned

Learned how to create and document a dedicated VirtualBox disk and partition,
and how to export a disk image for forensic testing.

## Problems encountered

Creating a raw image in the correct format and size required additional
validation. The team verified that the downloaded raw image matched the
recorded SHA-256 hash. The next step is to confirm the image's partition and
NTFS-volume layout with the parser.

## Plan for next week

- Prepare a known-file validation set and review parser results against the
  image.
- Create a validation manifest and parser-review notes.
- Document the baseline image's partition layout and support the next parser
  test cycle.
