# Source Code

Place all project source code in this folder. Commit working code at least weekly.

## Current tool

`ntfs_image_reader.py` reads the NTFS boot sector and first MFT record from a
disk image without modifying it. It reports the MFT byte offset and verifies
that the first record begins with the `FILE` signature. Run it from the
repository root with:

```powershell
python code/ntfs_image_reader.py path/to/image.dd
```
