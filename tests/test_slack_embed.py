"""Controlled copy and boundary verification without modifying real images."""

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
import slack_embed


class SlackEmbedTests(unittest.TestCase):
    def test_copy_changes_only_marker_range_across_chunk_boundary(self):
        with tempfile.TemporaryDirectory() as folder:
            source, destination = Path(folder) / "source.dd", Path(folder) / "working.dd"
            original = b"A" * 64
            source.write_bytes(original)
            with patch.object(slack_embed, "LAB_IMAGE_SHA256", hashlib.sha256(original).hexdigest().upper()), patch.object(slack_embed, "CHUNK_SIZE", 8):
                result = slack_embed.write_working_copy(source, destination, 7, b"TEST")
            expected = original[:7] + b"TEST" + original[11:]
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(destination.read_bytes(), expected)
            self.assertEqual(result["working_image_sha256"], hashlib.sha256(expected).hexdigest().upper())

    def test_refuses_existing_destination_and_source_as_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "source.dd"
            source.write_bytes(b"A" * 64)
            destination = Path(folder) / "existing.dd"
            destination.write_bytes(b"KEEP")
            for output in (source, destination):
                with self.assertRaises(ValueError):
                    slack_embed.write_working_copy(source, output, 1, b"TEST")
            self.assertEqual(destination.read_bytes(), b"KEEP")

    def test_unrecognized_source_is_not_patched(self):
        with tempfile.TemporaryDirectory() as folder:
            source, destination = Path(folder) / "source.dd", Path(folder) / "working.dd"
            original = b"A" * 64
            source.write_bytes(original)
            with self.assertRaisesRegex(ValueError, "Source hash"):
                slack_embed.write_working_copy(source, destination, 1, b"TEST")
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(destination.read_bytes(), original)

    def test_record_fixups_restore_sector_tails_and_reject_mismatch(self):
        record = bytearray(1024)
        record[4:6] = (48).to_bytes(2, "little")
        record[6:8] = (3).to_bytes(2, "little")
        record[48:54] = b"XXABCD"
        record[510:512] = record[1022:1024] = b"XX"
        restored = slack_embed.restore_record_fixups(bytes(record), 512)
        self.assertEqual(restored[510:512], b"AB")
        self.assertEqual(restored[1022:1024], b"CD")
        record[510:512] = b"NO"
        with self.assertRaises(ValueError):
            slack_embed.restore_record_fixups(bytes(record), 512)


if __name__ == "__main__":
    unittest.main()
