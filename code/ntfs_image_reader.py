"""Read and display the first sector of a disk image.

This is the first building block for the CSC-481 NTFS forensic parser.  It
opens an image only for reading and shows the first 512 bytes, where the boot
sector is found when the image begins directly with an NTFS volume.
"""

from __future__ import annotations

import argparse
from pathlib import Path


BOOT_SECTOR_SIZE = 512
BYTES_PER_LINE = 16


def format_hex(data: bytes) -> str:
    """Return a readable hexadecimal and ASCII view of *data*."""
    lines: list[str] = []

    for offset in range(0, len(data), BYTES_PER_LINE):
        chunk = data[offset : offset + BYTES_PER_LINE]
        hex_bytes = " ".join(f"{byte:02X}" for byte in chunk)
        ascii_bytes = "".join(
            chr(byte) if 32 <= byte <= 126 else "." for byte in chunk
        )
        lines.append(f"{offset:04X}  {hex_bytes:<47}  {ascii_bytes}")

    return "\n".join(lines)


def read_first_sector(image_path: Path) -> bytes:
    """Read exactly one 512-byte sector from an image without modifying it."""
    with image_path.open("rb") as image_file:
        sector = image_file.read(BOOT_SECTOR_SIZE)

    if len(sector) != BOOT_SECTOR_SIZE:
        raise ValueError(
            f"The image is only {len(sector)} bytes long; "
            f"it must contain at least {BOOT_SECTOR_SIZE} bytes."
        )

    return sector


def parse_ntfs_boot_sector(sector: bytes) -> dict[str, int | str | bool]:
    """Extract a few introductory NTFS boot-sector fields from *sector*."""
    bytes_per_sector = int.from_bytes(sector[0x0B:0x0D], byteorder="little")
    sectors_per_cluster = sector[0x0D]
    clusters_per_record = int.from_bytes(
        sector[0x40:0x41], byteorder="little", signed=True
    )

    if clusters_per_record < 0:
        mft_record_size = 2 ** abs(clusters_per_record)
    else:
        mft_record_size = clusters_per_record * bytes_per_sector * sectors_per_cluster

    return {
        "oem_id": sector[0x03:0x0B].decode("ascii", errors="replace").rstrip(),
        "ntfs_signature_valid": sector[0x03:0x0B] == b"NTFS    ",
        "bytes_per_sector": bytes_per_sector,
        "sectors_per_cluster": sectors_per_cluster,
        "bytes_per_cluster": bytes_per_sector * sectors_per_cluster,
        "total_sectors": int.from_bytes(sector[0x28:0x30], byteorder="little"),
        "mft_start_lcn": int.from_bytes(sector[0x30:0x38], byteorder="little"),
        "mft_mirror_lcn": int.from_bytes(sector[0x38:0x40], byteorder="little"),
        "mft_record_size": mft_record_size,
        "boot_signature_valid": sector[0x1FE:0x200] == b"\x55\xAA",
    }


def print_boot_sector_summary(boot_sector: dict[str, int | str | bool]) -> None:
    """Print a beginner-friendly summary of selected NTFS boot-sector fields."""
    print("Boot-sector summary")
    print(f"  OEM ID:               {boot_sector['oem_id']}")
    print(f"  NTFS signature valid: {boot_sector['ntfs_signature_valid']}")
    print(f"  Bytes per sector:     {boot_sector['bytes_per_sector']}")
    print(f"  Sectors per cluster:  {boot_sector['sectors_per_cluster']}")
    print(f"  Bytes per cluster:    {boot_sector['bytes_per_cluster']}")
    print(f"  Total sectors:        {boot_sector['total_sectors']}")
    print(f"  MFT start LCN:        {boot_sector['mft_start_lcn']}")
    print(f"  MFT mirror LCN:       {boot_sector['mft_mirror_lcn']}")
    print(f"  MFT record size:      {boot_sector['mft_record_size']} bytes")
    print(f"  Boot signature valid: {boot_sector['boot_signature_valid']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display the first 512 bytes of a disk image."
    )
    parser.add_argument("image", type=Path, help="path to a .dd disk image")
    args = parser.parse_args()

    if not args.image.is_file():
        parser.error(f"image file not found: {args.image}")

    try:
        first_sector = read_first_sector(args.image)
    except OSError as error:
        parser.error(f"could not read image: {error}")
    except ValueError as error:
        parser.error(str(error))

    print(f"Image: {args.image}")
    print(f"Read: {BOOT_SECTOR_SIZE} bytes (first sector)")
    print()
    boot_sector = parse_ntfs_boot_sector(first_sector)
    if not boot_sector["ntfs_signature_valid"]:
        print("Warning: this does not appear to be an NTFS boot sector.")
        print("The raw hex view is shown below, but NTFS values may not be meaningful.")
        print()

    print_boot_sector_summary(boot_sector)
    print()
    print("Offset  Hex bytes                                        ASCII")
    print(format_hex(first_sector))


if __name__ == "__main__":
    main()
