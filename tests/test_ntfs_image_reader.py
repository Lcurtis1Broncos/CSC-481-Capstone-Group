"""Repeatable tests for the first NTFS image-reader functions."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "code"))

from ntfs_image_reader import (
    BOOT_SECTOR_SIZE,
    MBR_PARTITION_TABLE_OFFSET,
    calculate_absolute_mft_byte_offset,
    calculate_mft_byte_offset,
    find_windows_data_partition,
    parse_mft_record_header,
    parse_mbr_partitions,
    parse_ntfs_boot_sector,
    read_first_sector,
    read_mft_record,
    read_sector_at_offset,
)


def make_boot_sector(
    *,
    bytes_per_sector: int,
    sectors_per_cluster: int,
    mft_lcn: int,
    volume_serial: bytes = b"\x01\x02\x03\x04\x05\x06\x07\x08",
) -> bytes:
    """Create a minimal, harmless NTFS-shaped sector for parser testing."""
    sector = bytearray(BOOT_SECTOR_SIZE)
    sector[0x03:0x0B] = b"NTFS    "
    sector[0x0B:0x0D] = bytes_per_sector.to_bytes(2, byteorder="little")
    sector[0x0D] = sectors_per_cluster
    sector[0x28:0x30] = (100_000).to_bytes(8, byteorder="little")
    sector[0x30:0x38] = mft_lcn.to_bytes(8, byteorder="little")
    sector[0x38:0x40] = (4).to_bytes(8, byteorder="little")
    sector[0x40] = 1
    sector[0x48:0x50] = volume_serial
    sector[0x1FE:0x200] = b"\x55\xAA"
    return bytes(sector)


def make_mft_record(*, record_size: int, flags: int = 0x0001) -> bytes:
    """Create a minimal MFT-shaped record for reader testing."""
    record = bytearray(record_size)
    record[0x00:0x04] = b"FILE"
    record[0x14:0x16] = (56).to_bytes(2, byteorder="little")
    record[0x16:0x18] = flags.to_bytes(2, byteorder="little")
    return bytes(record)


def make_mbr_sector(*, start_lba: int, total_sectors: int) -> bytes:
    """Create a minimal MBR with one Windows-data partition entry."""
    sector = bytearray(BOOT_SECTOR_SIZE)
    entry = MBR_PARTITION_TABLE_OFFSET
    sector[entry + 0x04] = 0x07
    sector[entry + 0x08 : entry + 0x0C] = start_lba.to_bytes(4, byteorder="little")
    sector[entry + 0x0C : entry + 0x10] = total_sectors.to_bytes(
        4, byteorder="little"
    )
    sector[0x1FE:0x200] = b"\x55\xAA"
    return bytes(sector)


class NtfsImageReaderTests(unittest.TestCase):
    def test_parses_1024_byte_clusters(self) -> None:
        sector = make_boot_sector(
            bytes_per_sector=512, sectors_per_cluster=2, mft_lcn=2005
        )

        result = parse_ntfs_boot_sector(sector)

        self.assertTrue(result["ntfs_signature_valid"])
        self.assertEqual(result["bytes_per_cluster"], 1024)
        self.assertEqual(result["mft_start_lcn"], 2005)
        self.assertEqual(result["mft_record_size"], 1024)

    def test_parses_4096_byte_clusters(self) -> None:
        sector = make_boot_sector(
            bytes_per_sector=512, sectors_per_cluster=8, mft_lcn=786_432
        )

        result = parse_ntfs_boot_sector(sector)

        self.assertEqual(result["bytes_per_cluster"], 4096)
        self.assertEqual(result["mft_start_lcn"], 786_432)
        self.assertEqual(result["mft_record_size"], 4096)

    def test_parses_the_volume_serial_number(self) -> None:
        sector = make_boot_sector(
            bytes_per_sector=512,
            sectors_per_cluster=8,
            mft_lcn=786_432,
            volume_serial=b"\x12\x34\x56\x78\x9A\xBC\xDE\xF0",
        )

        result = parse_ntfs_boot_sector(sector)

        self.assertEqual(result["volume_serial"], "F0DEBC9A78563412")

    def test_rejects_an_image_shorter_than_one_sector(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            short_image = Path(directory) / "too_short.dd"
            short_image.write_bytes(b"not a complete sector")

            with self.assertRaises(ValueError):
                read_first_sector(short_image)

    def test_calculates_first_mft_record_offset(self) -> None:
        boot_sector = parse_ntfs_boot_sector(
            make_boot_sector(
                bytes_per_sector=512, sectors_per_cluster=2, mft_lcn=2005
            )
        )

        self.assertEqual(calculate_mft_byte_offset(boot_sector), 2_053_120)

    def test_calculates_mft_offset_inside_a_full_disk_image(self) -> None:
        boot_sector = parse_ntfs_boot_sector(
            make_boot_sector(
                bytes_per_sector=512, sectors_per_cluster=8, mft_lcn=786_432
            )
        )

        result = calculate_absolute_mft_byte_offset(boot_sector, 1_048_576)

        self.assertEqual(result, 3_222_274_048)

    def test_parses_and_selects_a_windows_data_partition(self) -> None:
        partitions = parse_mbr_partitions(
            make_mbr_sector(start_lba=2048, total_sectors=16_771_072)
        )

        result = find_windows_data_partition(partitions)

        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result["number"], 1)
        self.assertEqual(result["partition_type"], 0x07)
        self.assertEqual(result["start_lba"], 2048)
        self.assertEqual(result["byte_offset"], 1_048_576)

    def test_reads_a_sector_at_a_specific_offset(self) -> None:
        target_sector = b"A" * BOOT_SECTOR_SIZE
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "test.dd"
            image_path.write_bytes(b"X" * BOOT_SECTOR_SIZE + target_sector)

            result = read_sector_at_offset(image_path, BOOT_SECTOR_SIZE)

        self.assertEqual(result, target_sector)

    def test_reads_and_parses_a_valid_mft_record(self) -> None:
        record = make_mft_record(record_size=1024)

        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "test.dd"
            image_path.write_bytes(b"\x00" * 64 + record)

            result = read_mft_record(image_path, 64, 1024)
            header = parse_mft_record_header(result)

        self.assertTrue(header["signature_valid"])
        self.assertEqual(header["first_attribute_offset"], 56)
        self.assertTrue(header["in_use"])
        self.assertFalse(header["is_directory"])

    def test_identifies_an_invalid_mft_signature(self) -> None:
        header = parse_mft_record_header(b"NOPE" + b"\x00" * 20)

        self.assertFalse(header["signature_valid"])


if __name__ == "__main__":
    unittest.main()
