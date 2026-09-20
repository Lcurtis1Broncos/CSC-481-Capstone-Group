# Weekly Journal - Lucas Curtis

**Week:** 5  
**Reporting period:** September 14  - September 20, 2026

## Work completed

- Created another dedicated VirtualBox baseline disk for the project.
- The last baseline disk was still encrypted by BitLocker.
- Decrypted the disk and verified BitLocker was no longer active on the drive.
- Created and shared a full raw disk image for team testing, then recorded its
  SHA-256 hash.

## What I learned

I learned to check and deactivate BitLocker for specific disk volumes when needed. I did not account for BitLocker when creating the first disk image.

## Problems encountered

Deactivating BitLocker and getting a new image for the baseline wasn't too hard, but it wasn't expected by me; I should've taken BitLocker into account
when creating the first baseline image.

## Plan for next week

- Prepare a known-file validation set and review parser results against the
  image.
- Create a validation manifest and parser-review notes.
- Document the baseline image's partition layout and support the next parser
  test cycle.
