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
    calculate_mft_byte_offset,
    parse_mft_record_header,
    parse_ntfs_boot_sector,
    read_first_sector,
    read_mft_record,
)


def make_boot_sector(
    *, bytes_per_sector: int, sectors_per_cluster: int, mft_lcn: int
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
    sector[0x1FE:0x200] = b"\x55\xAA"
    return bytes(sector)


def make_mft_record(*, record_size: int, flags: int = 0x0001) -> bytes:
    """Create a minimal MFT-shaped record for reader testing."""
    record = bytearray(record_size)
    record[0x00:0x04] = b"FILE"
    record[0x14:0x16] = (56).to_bytes(2, byteorder="little")
    record[0x16:0x18] = flags.to_bytes(2, byteorder="little")
    return bytes(record)


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
