"""Read introductory NTFS information from a volume or full-disk image.

The reader is intentionally read-only.  It supports images that begin with an
NTFS boot sector and full-disk images that begin with an MBR partition table.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime, timedelta
from pathlib import Path


BOOT_SECTOR_SIZE = 512
BYTES_PER_LINE = 16
MFT_RECORD_SIGNATURE = b"FILE"
MBR_PARTITION_TABLE_OFFSET = 0x1BE
MBR_PARTITION_ENTRY_SIZE = 16
MBR_PARTITION_COUNT = 4
MBR_SIGNATURE = b"\x55\xAA"
WINDOWS_DATA_PARTITION_TYPE = 0x07
ATTRIBUTE_TYPE_STANDARD_INFORMATION = 0x10
ATTRIBUTE_TYPE_FILE_NAME = 0x30
ATTRIBUTE_TYPE_DATA = 0x80
ATTRIBUTE_TYPE_END = 0xFFFFFFFF

# ANSI escape codes are understood by the VS Code terminal and make recovered
# filenames easier to spot without changing the forensic data being displayed.
ANSI_YELLOW = "\033[33m"
ANSI_RESET = "\033[0m"


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
    return read_sector_at_offset(image_path, 0)


def read_sector_at_offset(image_path: Path, byte_offset: int) -> bytes:
    """Read one 512-byte sector at *byte_offset* without modifying an image."""
    with image_path.open("rb") as image_file:
        image_file.seek(byte_offset)
        sector = image_file.read(BOOT_SECTOR_SIZE)

    if len(sector) != BOOT_SECTOR_SIZE:
        raise ValueError(
            "The image does not contain a complete 512-byte sector at "
            f"byte offset {byte_offset}."
        )

    return sector


def parse_mbr_partitions(sector: bytes) -> list[dict[str, int | bool]]:
    """Return the populated entries from a standard MBR partition table."""
    if len(sector) != BOOT_SECTOR_SIZE:
        raise ValueError("An MBR sector must contain exactly 512 bytes.")

    partitions: list[dict[str, int | bool]] = []
    for index in range(MBR_PARTITION_COUNT):
        entry_offset = MBR_PARTITION_TABLE_OFFSET + index * MBR_PARTITION_ENTRY_SIZE
        entry = sector[entry_offset : entry_offset + MBR_PARTITION_ENTRY_SIZE]
        partition_type = entry[0x04]
        total_sectors = int.from_bytes(entry[0x0C:0x10], byteorder="little")
        if partition_type == 0 or total_sectors == 0:
            continue

        start_lba = int.from_bytes(entry[0x08:0x0C], byteorder="little")
        partitions.append(
            {
                "number": index + 1,
                "bootable": entry[0x00] == 0x80,
                "partition_type": partition_type,
                "start_lba": start_lba,
                "total_sectors": total_sectors,
                "byte_offset": start_lba * BOOT_SECTOR_SIZE,
            }
        )

    return partitions


def find_windows_data_partition(
    partitions: list[dict[str, int | bool]],
) -> dict[str, int | bool] | None:
    """Return the first MBR type 0x07 partition, if present.

    Type 0x07 is a Windows data-partition hint.  The caller still verifies the
    NTFS boot-sector signature before treating it as an NTFS volume.
    """
    return next(
        (
            partition
            for partition in partitions
            if partition["partition_type"] == WINDOWS_DATA_PARTITION_TYPE
        ),
        None,
    )


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
        "volume_serial": f"{int.from_bytes(sector[0x48:0x50], byteorder='little'):016X}",
        "boot_signature_valid": sector[0x1FE:0x200] == b"\x55\xAA",
    }


def calculate_mft_byte_offset(boot_sector: dict[str, int | str | bool]) -> int:
    """Return the first MFT record's byte offset for a volume image."""
    return int(boot_sector["mft_start_lcn"]) * int(boot_sector["bytes_per_cluster"])


def calculate_absolute_mft_byte_offset(
    boot_sector: dict[str, int | str | bool], ntfs_partition_offset: int
) -> int:
    """Return the first MFT record offset in a full-disk image."""
    return ntfs_partition_offset + calculate_mft_byte_offset(boot_sector)


def read_mft_record(image_path: Path, byte_offset: int, record_size: int) -> bytes:
    """Read one MFT record without modifying the image."""
    with image_path.open("rb") as image_file:
        image_file.seek(byte_offset)
        record = image_file.read(record_size)

    if len(record) != record_size:
        raise ValueError(
            "The image does not contain a complete MFT record at "
            f"byte offset {byte_offset}."
        )

    return record


def parse_mft_record_header(record: bytes) -> dict[str, int | str | bool]:
    """Extract a few introductory fields from an MFT record header."""
    if len(record) < 24:
        raise ValueError("An MFT record header must contain at least 24 bytes.")

    flags = int.from_bytes(record[0x16:0x18], byteorder="little")
    return {
        "signature": record[0x00:0x04].decode("ascii", errors="replace"),
        "signature_valid": record[0x00:0x04] == MFT_RECORD_SIGNATURE,
        "first_attribute_offset": int.from_bytes(
            record[0x14:0x16], byteorder="little"
        ),
        "in_use": bool(flags & 0x0001),
        "is_directory": bool(flags & 0x0002),
    }


def parse_mft_attributes(record: bytes) -> list[dict[str, int | str | bytes | bool]]:
    """Return the valid attributes stored in an MFT record.

    Each attribute begins with a type and a length.  The length lets the reader
    move safely to the next attribute instead of assuming a fixed layout.
    """
    header = parse_mft_record_header(record)
    if not header["signature_valid"]:
        return []

    attribute_offset = int(header["first_attribute_offset"])
    attributes: list[dict[str, int | str | bytes | bool]] = []

    while attribute_offset + 8 <= len(record):
        attribute_type = int.from_bytes(
            record[attribute_offset : attribute_offset + 4], byteorder="little"
        )
        if attribute_type == ATTRIBUTE_TYPE_END:
            break

        attribute_length = int.from_bytes(
            record[attribute_offset + 4 : attribute_offset + 8],
            byteorder="little",
        )
        if attribute_length < 16 or attribute_offset + attribute_length > len(record):
            raise ValueError("MFT attribute has an invalid length.")

        non_resident = bool(record[attribute_offset + 8])
        name_length = record[attribute_offset + 0x09]
        name_offset = int.from_bytes(
            record[attribute_offset + 0x0A : attribute_offset + 0x0C],
            byteorder="little",
        )
        attribute_name = ""
        if name_length:
            name_start = attribute_offset + name_offset
            name_end = name_start + name_length * 2
            if name_offset < 0x10 or name_end > attribute_offset + attribute_length:
                raise ValueError("MFT attribute has an invalid name range.")
            attribute_name = record[name_start:name_end].decode(
                "utf-16-le", errors="replace"
            )

        attribute: dict[str, int | str | bytes | bool] = {
            "type": attribute_type,
            "length": attribute_length,
            "offset": attribute_offset,
            "non_resident": non_resident,
            "name": attribute_name,
        }

        if not non_resident:
            value_length = int.from_bytes(
                record[attribute_offset + 0x10 : attribute_offset + 0x14],
                byteorder="little",
            )
            value_offset = int.from_bytes(
                record[attribute_offset + 0x14 : attribute_offset + 0x16],
                byteorder="little",
            )
            value_start = attribute_offset + value_offset
            value_end = value_start + value_length
            if (
                value_offset < 0x18
                or value_end > attribute_offset + attribute_length
            ):
                raise ValueError("Resident MFT attribute has an invalid value range.")
            attribute["value"] = record[value_start:value_end]
        else:
            if attribute_length < 0x40:
                raise ValueError("Non-resident MFT attribute is too short.")
            attribute["allocated_size"] = int.from_bytes(
                record[attribute_offset + 0x28 : attribute_offset + 0x30],
                byteorder="little",
            )
            attribute["real_size"] = int.from_bytes(
                record[attribute_offset + 0x30 : attribute_offset + 0x38],
                byteorder="little",
            )

        attributes.append(attribute)
        attribute_offset += attribute_length

    return attributes


def parse_file_name_attribute(
    attribute: dict[str, int | str | bytes | bool],
) -> dict[str, int | str]:
    """Decode the resident contents of an NTFS ``$FILE_NAME`` attribute."""
    if attribute["type"] != ATTRIBUTE_TYPE_FILE_NAME:
        raise ValueError("The supplied attribute is not a $FILE_NAME attribute.")
    if attribute["non_resident"]:
        raise ValueError("A $FILE_NAME attribute must be resident in its MFT record.")

    value = attribute.get("value")
    if not isinstance(value, bytes) or len(value) < 0x42:
        raise ValueError("$FILE_NAME attribute is too short.")

    name_length = value[0x40]
    name_start = 0x42
    name_end = name_start + name_length * 2
    if name_end > len(value):
        raise ValueError("$FILE_NAME attribute has an invalid name length.")

    return {
        "name": value[name_start:name_end].decode("utf-16-le", errors="replace"),
        "name_length": name_length,
        "namespace": value[0x41],
        "allocated_size": int.from_bytes(value[0x28:0x30], byteorder="little"),
        "real_size": int.from_bytes(value[0x30:0x38], byteorder="little"),
    }


def format_filetime(filetime: int) -> str:
    """Return a UTC timestamp for a Windows FILETIME value."""
    if filetime == 0:
        return "Not set"

    try:
        filetime_epoch = datetime(1601, 1, 1, tzinfo=UTC)
        timestamp = filetime_epoch + timedelta(microseconds=filetime // 10)
    except OverflowError:
        return f"Invalid FILETIME ({filetime})"

    return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")


def describe_file_attributes(flags: int) -> str:
    """Return the common Windows file-attribute flags in plain language."""
    names = {
        0x0001: "Read-only",
        0x0002: "Hidden",
        0x0004: "System",
        0x0020: "Archive",
        0x0800: "Compressed",
        0x1000: "Offline",
        0x2000: "Not content indexed",
        0x4000: "Encrypted",
    }
    descriptions = [name for bit, name in names.items() if flags & bit]
    return ", ".join(descriptions) if descriptions else "None recorded"


def parse_standard_information_attribute(
    attribute: dict[str, int | str | bytes | bool],
) -> dict[str, int | str]:
    """Decode the basic timestamps and flags in ``$STANDARD_INFORMATION``."""
    if attribute["type"] != ATTRIBUTE_TYPE_STANDARD_INFORMATION:
        raise ValueError("The supplied attribute is not $STANDARD_INFORMATION.")
    if attribute["non_resident"]:
        raise ValueError("$STANDARD_INFORMATION must be resident in its MFT record.")

    value = attribute.get("value")
    if not isinstance(value, bytes) or len(value) < 0x24:
        raise ValueError("$STANDARD_INFORMATION attribute is too short.")

    flags = int.from_bytes(value[0x20:0x24], byteorder="little")
    return {
        "created": format_filetime(int.from_bytes(value[0x00:0x08], byteorder="little")),
        "modified": format_filetime(int.from_bytes(value[0x08:0x10], byteorder="little")),
        "mft_modified": format_filetime(
            int.from_bytes(value[0x10:0x18], byteorder="little")
        ),
        "accessed": format_filetime(int.from_bytes(value[0x18:0x20], byteorder="little")),
        "file_attributes": flags,
        "file_attribute_names": describe_file_attributes(flags),
    }


def parse_data_attribute(
    attribute: dict[str, int | str | bytes | bool],
) -> dict[str, int | str | bool | None]:
    """Summarize a normal or named ``$DATA`` attribute without reading content."""
    if attribute["type"] != ATTRIBUTE_TYPE_DATA:
        raise ValueError("The supplied attribute is not a $DATA attribute.")

    stream_name = str(attribute["name"])
    if attribute["non_resident"]:
        return {
            "stream_name": stream_name,
            "resident": False,
            "logical_size": int(attribute["real_size"]),
            "allocated_size": int(attribute["allocated_size"]),
        }

    value = attribute.get("value")
    if not isinstance(value, bytes):
        raise ValueError("Resident $DATA attribute does not contain a value.")
    return {
        "stream_name": stream_name,
        "resident": True,
        "logical_size": len(value),
        "allocated_size": None,
    }


def get_mft_record_offset(
    mft_byte_offset: int, record_size: int, record_number: int
) -> int:
    """Return the absolute disk-image offset for an MFT record number."""
    if record_number < 0:
        raise ValueError("An MFT record number cannot be negative.")
    return mft_byte_offset + record_number * record_size


def list_mft_file_names(
    image_path: Path,
    mft_byte_offset: int,
    record_size: int,
    maximum_records: int,
) -> list[dict[str, int | str | bool]]:
    """Read up to *maximum_records* MFT records and return their file names."""
    results: list[dict[str, int | str | bool]] = []

    with image_path.open("rb") as image_file:
        image_file.seek(mft_byte_offset)
        for record_number in range(maximum_records):
            record = image_file.read(record_size)
            if len(record) != record_size:
                break

            header = parse_mft_record_header(record)
            if not header["signature_valid"] or not header["in_use"]:
                continue

            try:
                attributes = parse_mft_attributes(record)
            except ValueError:
                continue

            for attribute in attributes:
                if attribute["type"] != ATTRIBUTE_TYPE_FILE_NAME:
                    continue
                try:
                    file_name = parse_file_name_attribute(attribute)
                except ValueError:
                    continue
                results.append(
                    {
                        "record_number": record_number,
                        "name": str(file_name["name"]),
                        "namespace": int(file_name["namespace"]),
                        "is_directory": bool(header["is_directory"]),
                    }
                )

    return results


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
    print(f"  Volume serial:        {boot_sector['volume_serial']}")
    print(f"  Boot signature valid: {boot_sector['boot_signature_valid']}")


def print_partition_summary(partition: dict[str, int | bool]) -> None:
    """Print the MBR values used to locate the candidate NTFS volume."""
    print("MBR partition summary")
    print(f"  Partition number:     {partition['number']}")
    print(f"  Bootable:             {partition['bootable']}")
    print(f"  Partition type:       0x{int(partition['partition_type']):02X}")
    print(f"  Start LBA:            {partition['start_lba']}")
    print(f"  NTFS boot offset:     {partition['byte_offset']}")


def print_mft_record_summary(
    byte_offset: int, record_size: int, record_header: dict[str, int | str | bool]
) -> None:
    """Print a beginner-friendly summary of the first MFT record."""
    print("First MFT record summary")
    print("  Record number:        0 ($Mft)")
    print(f"  Byte offset:          {byte_offset}")
    print(f"  Record size:          {record_size} bytes")
    print(f"  Record signature:     {record_header['signature']}")
    print(f"  FILE signature valid: {record_header['signature_valid']}")
    print(f"  First attribute:      byte {record_header['first_attribute_offset']}")
    print(f"  Record in use:        {record_header['in_use']}")
    print(f"  Is directory:         {record_header['is_directory']}")


def print_file_name_listing(file_names: list[dict[str, int | str | bool]]) -> None:
    """Print the file names decoded from a selected range of MFT records."""
    print("MFT file-name listing")
    if not file_names:
        print("  No in-use $FILE_NAME attributes were decoded in this range.")
        return

    for file_name in file_names:
        item_type = "directory" if file_name["is_directory"] else "file"
        highlighted_name = f"{ANSI_YELLOW}{file_name['name']}{ANSI_RESET}"
        print(
            f"  Record {file_name['record_number']}: {highlighted_name} "
            f"({item_type}, namespace {file_name['namespace']})"
        )


def print_attribute_summary(record_number: int, record: bytes) -> None:
    """Print beginner-friendly summaries of selected MFT attribute types."""
    record_header = parse_mft_record_header(record)
    print(f"MFT record {record_number} attribute summary")
    print(f"  FILE signature valid: {record_header['signature_valid']}")
    print(f"  Record in use:        {record_header['in_use']}")

    attributes = parse_mft_attributes(record)
    if not attributes:
        print("  No attributes were decoded.")
        return

    for attribute in attributes:
        attribute_type = attribute["type"]
        if attribute_type == ATTRIBUTE_TYPE_STANDARD_INFORMATION:
            standard_information = parse_standard_information_attribute(attribute)
            print("\n  $STANDARD_INFORMATION")
            print(f"    Created:         {standard_information['created']}")
            print(f"    Modified:        {standard_information['modified']}")
            print(f"    File attributes: {standard_information['file_attribute_names']}")
        elif attribute_type == ATTRIBUTE_TYPE_FILE_NAME:
            file_name = parse_file_name_attribute(attribute)
            print("\n  $FILE_NAME")
            print(f"    Name:            {ANSI_YELLOW}{file_name['name']}{ANSI_RESET}")
            print(f"    Logical size:    {file_name['real_size']} bytes")
            print(f"    Allocated size:  {file_name['allocated_size']} bytes")
        elif attribute_type == ATTRIBUTE_TYPE_DATA:
            data = parse_data_attribute(attribute)
            stream_name = data["stream_name"] or "[unnamed]"
            print("\n  $DATA")
            print(f"    Stream name:     {stream_name}")
            print(f"    Resident:        {data['resident']}")
            print(f"    Logical size:    {data['logical_size']} bytes")
            if data["allocated_size"] is None:
                print("    Allocated size:  resident in MFT record")
            else:
                print(f"    Allocated size:  {data['allocated_size']} bytes")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display introductory NTFS information from a disk image."
    )
    parser.add_argument("image", type=Path, help="path to a .dd disk image")
    parser.add_argument(
        "--list-files",
        type=int,
        metavar="RECORDS",
        help="scan this many MFT records and display decoded file names",
    )
    parser.add_argument(
        "--show-record",
        type=int,
        action="append",
        metavar="NUMBER",
        help="display an attribute summary; repeat this option for more records",
    )
    args = parser.parse_args()

    if not args.image.is_file():
        parser.error(f"image file not found: {args.image}")

    try:
        first_sector = read_first_sector(args.image)
    except OSError as error:
        parser.error(f"could not read image: {error}")
    except ValueError as error:
        parser.error(str(error))

    ntfs_boot_offset = 0
    partition: dict[str, int | bool] | None = None
    boot_sector = parse_ntfs_boot_sector(first_sector)

    if not boot_sector["ntfs_signature_valid"]:
        try:
            partition = find_windows_data_partition(parse_mbr_partitions(first_sector))
            if partition is not None:
                ntfs_boot_offset = int(partition["byte_offset"])
                boot_sector_sector = read_sector_at_offset(args.image, ntfs_boot_offset)
                boot_sector = parse_ntfs_boot_sector(boot_sector_sector)
        except OSError as error:
            parser.error(f"could not read the partition boot sector: {error}")
        except ValueError as error:
            parser.error(str(error))

    print(f"Image: {args.image}")
    print(f"Read: {BOOT_SECTOR_SIZE} bytes (first sector)")
    print()

    if partition is not None:
        print_partition_summary(partition)
        print()

    if not boot_sector["ntfs_signature_valid"]:
        print("Warning: no verified NTFS boot sector was found.")
        print("The raw hex view of the first sector is shown below.")
        print()

    print_boot_sector_summary(boot_sector)
    print()

    if boot_sector["ntfs_signature_valid"]:
        mft_byte_offset = calculate_absolute_mft_byte_offset(
            boot_sector, ntfs_boot_offset
        )
        try:
            first_mft_record = read_mft_record(
                args.image,
                mft_byte_offset,
                int(boot_sector["mft_record_size"]),
            )
        except OSError as error:
            parser.error(f"could not read the MFT record: {error}")
        except ValueError as error:
            parser.error(str(error))

        print_mft_record_summary(
            mft_byte_offset,
            int(boot_sector["mft_record_size"]),
            parse_mft_record_header(first_mft_record),
        )
        print()

        if args.list_files is not None:
            if args.list_files < 1:
                parser.error("--list-files must be at least 1")
            try:
                file_names = list_mft_file_names(
                    args.image,
                    mft_byte_offset,
                    int(boot_sector["mft_record_size"]),
                    args.list_files,
                )
            except OSError as error:
                parser.error(f"could not scan MFT records: {error}")
            print_file_name_listing(file_names)
            print()

        if args.show_record is not None:
            for record_number in args.show_record:
                try:
                    selected_record_offset = get_mft_record_offset(
                        mft_byte_offset,
                        int(boot_sector["mft_record_size"]),
                        record_number,
                    )
                    selected_record = read_mft_record(
                        args.image,
                        selected_record_offset,
                        int(boot_sector["mft_record_size"]),
                    )
                    print_attribute_summary(record_number, selected_record)
                except (OSError, ValueError) as error:
                    parser.error(str(error))
                print()

    print("Offset  Hex bytes                                        ASCII")
    print(format_hex(first_sector))


if __name__ == "__main__":
    main()
