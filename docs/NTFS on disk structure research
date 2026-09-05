NTFS on-disk structures research

NTFS stores file-system metadata primarily through special metadata files. The most important structures for a forensic investigation are:

| Structure  | Purpose / forensic value                                                                                                                                       |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$MFT`     | Master File Table; contains at least one record for every file and directory. MFT records contain attributes describing the file.                              |
| `$MFTMirr` | Backup copy of the first four MFT records.                                                                                                                     |
| `$Boot`    | Contains the NTFS boot record/volume boot information.                                                                                                         |
| `$Bitmap`  | Tracks which clusters on the volume are allocated or free.                                                                                                     |
| `$LogFile` | NTFS transactional/logging information used for file-system recovery.                                                                                          |
| `$Volume`  | Contains volume information such as the serial number, creation information, and dirty flag.                                                                   | 
| `$AttrDef` | Defines NTFS attribute types.                                                                                                                                  |
| `$BadClus` | Identifies clusters marked as bad.                                                                                                                             |
| `$Secure`  | Stores security descriptors used by the volume.                                                                                                                |
| `$UpCase`  | Contains the uppercase-character mapping table used by NTFS.                                                                                                   |
| `$Extend`  | Directory containing additional NTFS metadata, including structures related to reparse points, object IDs, quotas, and other functions.                        |


The MFT record is particularly important. Microsoft documents it as a fixed-size file record segment; the MS-FSCC specification identifies an NTFS file record segment as 1,024 bytes.

MFT records contain attributes such as:

$STANDARD_INFORMATION — timestamps and file attributes
$FILE_NAME — filename information
$DATA — file contents
$ATTRIBUTE_LIST — references additional attributes/records
$INDEX_ROOT / $INDEX_ALLOCATION — directory indexing
$BITMAP — allocation information for indexes
$REPARSE_POINT — reparse-point information
