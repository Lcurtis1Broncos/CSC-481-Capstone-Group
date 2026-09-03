"""Repeatable tests for the first NTFS image-reader functions."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "code"))

from ntfs_image_reader import BOOT_SECTOR_SIZE, parse_ntfs_boot_sector, read_first_sector


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


if __name__ == "__main__":
    unittest.main()
