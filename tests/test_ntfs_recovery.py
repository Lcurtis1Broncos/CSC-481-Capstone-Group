"""Synthetic image tests: no dependence on the team's multi-gigabyte images."""

import hashlib
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from ntfs_recovery import locate_stream, iter_stream_content, recover_stream, recover_with_report
from test_ntfs_image_reader import (
    make_boot_sector, make_resident_attribute, make_nonresident_data_attribute,
    make_record_with_attributes, make_mbr_sector,
)


def disk_record(*attributes, flags=1, extension=False):
    record = bytearray(make_record_with_attributes(*attributes))
    used = 56 + sum(map(len, attributes)) + 4
    record[0x18:0x1C] = used.to_bytes(4, "little")
    record[0x16:0x18] = flags.to_bytes(2, "little")
    if extension:
        record[0x20] = 1
    record[4:6] = (0x30).to_bytes(2, "little")
    record[6:8] = (3).to_bytes(2, "little")
    record[0x30:0x32] = b"\xab\xcd"
    for index in (1, 2):
        tail = index * 512 - 2
        record[0x30 + 2 * index:0x32 + 2 * index] = record[tail:tail + 2]
        record[tail:tail + 2] = b"\xab\xcd"
    return bytes(record)


def nonresident(*, size=700, initialized=None, mapping=b"\x11\x01\x14\x11\x01\xf6\x00",
                allocated=1024, flags=0, start=0, end=1):
    attribute = bytearray(make_nonresident_data_attribute(
        logical_size=size, allocated_size=allocated, mapping_pairs=mapping))
    attribute[0x0C:0x0E] = flags.to_bytes(2, "little")
    attribute[0x10:0x18] = start.to_bytes(8, "little")
    attribute[0x18:0x20] = end.to_bytes(8, "little")
    attribute[0x38:0x40] = (size if initialized is None else initialized).to_bytes(8, "little")
    return bytes(attribute)


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.image = self.root / "lab.dd"

    def image_bytes(self, *attributes, partition_offset=0, record_flags=1, extension=False,
                    mft_mapping=b"\x11\x08\x04\x00"):
        image = bytearray(64 * 512)
        boot = bytearray(make_boot_sector(bytes_per_sector=512, sectors_per_cluster=1, mft_lcn=4))
        boot[0x28:0x30] = (64).to_bytes(8, "little")
        boot[0x40] = 246  # -10 => 1024-byte records
        image[:512] = boot
        mft = nonresident(size=4096, mapping=mft_mapping, allocated=4096, end=7)
        image[2048:3072] = disk_record(mft)
        image[3072:4096] = disk_record(*attributes, flags=record_flags, extension=extension)
        image[20 * 512:21 * 512] = b"A" * 512
        image[10 * 512:11 * 512] = b"B" * 512
        if partition_offset:
            prefix = bytearray(partition_offset)
            prefix[:512] = make_mbr_sector(start_lba=partition_offset // 512, total_sectors=64)
            image = prefix + image
        self.image.write_bytes(image)
        return bytes(image)

    def content(self, stream=""):
        return b"".join(iter_stream_content(locate_stream(self.image, 1, stream)))

    def test_resident_crosses_sector_tail_and_recovers_original_bytes(self):
        payload = bytes(range(256)) * 2
        original = self.image_bytes(make_resident_attribute(0x80, payload))
        result = recover_stream(locate_stream(self.image, 1), self.root / "payload.bin")
        self.assertEqual((self.root / "payload.bin").read_bytes(), payload)
        self.assertEqual(result["recovered_sha256"], hashlib.sha256(payload).hexdigest().upper())
        self.assertEqual(self.image.read_bytes(), original)

    def test_named_stream_selection_is_exact(self):
        self.image_bytes(make_resident_attribute(0x80, b"host"),
                         make_resident_attribute(0x80, b"hidden", name="Evidence"))
        self.assertEqual(self.content(), b"host")
        self.assertEqual(self.content("Evidence"), b"hidden")
        with self.assertRaises(ValueError):
            self.content("Missing")

    def test_fragmented_nonresident_content_excludes_slack_and_preserves_run_order(self):
        self.image_bytes(nonresident())
        location = locate_stream(self.image, 1)
        self.assertEqual(self.content(), b"A" * 512 + b"B" * 188)
        self.assertEqual(location.extents, ((10240, 512), (5120, 512)))
        self.assertEqual(location.slack["byte_offset"], 5120 + 188)
        self.assertEqual(location.slack["length"], 324)

    def test_uninitialized_bytes_are_zero_not_disk_contents(self):
        self.image_bytes(nonresident(initialized=520))
        self.assertEqual(self.content(), b"A" * 512 + b"B" * 8 + bytes(180))

    def test_mbr_offsets_include_partition_start(self):
        self.image_bytes(nonresident(), partition_offset=1024)
        location = locate_stream(self.image, 1)
        self.assertEqual(location.record_offset, 4096)
        self.assertEqual(location.extents[0][0], 11264)
        self.assertEqual(self.content(), b"A" * 512 + b"B" * 188)

    def test_refuses_existing_destination_and_source_as_destination(self):
        original = self.image_bytes(make_resident_attribute(0x80, b"test"))
        output = self.root / "existing"
        output.write_bytes(b"keep")
        for destination in (self.image, output):
            with self.assertRaises(ValueError):
                recover_stream(locate_stream(self.image, 1), destination)
        self.assertEqual(output.read_bytes(), b"keep")
        self.assertEqual(self.image.read_bytes(), original)

    def test_refuses_invalid_or_unsupported_streams(self):
        cases = [nonresident(flags=f) for f in (1, 0x4000, 0x8000)]
        cases += [nonresident(start=1), nonresident(size=1025),
                  nonresident(initialized=701), nonresident(allocated=512),
                  nonresident(end=2),
                  nonresident(mapping=b"\x01\x02\x00"),
                  nonresident(mapping=b"\x11\x02\x3f\x00"),
                  nonresident(mapping=b"\x19\x01\x00")]
        for attribute in cases:
            with self.subTest(attribute=attribute.hex()):
                self.image_bytes(attribute)
                with self.assertRaises(ValueError):
                    locate_stream(self.image, 1)

    def test_refuses_duplicate_streams_and_attribute_lists(self):
        data = make_resident_attribute(0x80, b"test")
        for attributes in ((data, data), (data, make_resident_attribute(0x20, b"list"))):
            self.image_bytes(*attributes)
            with self.assertRaises(ValueError):
                locate_stream(self.image, 1)

    def test_refuses_deleted_directory_and_extension_records(self):
        for options in ({"record_flags": 0}, {"record_flags": 3}, {"extension": True}):
            self.image_bytes(make_resident_attribute(0x80, b"test"), **options)
            with self.assertRaises(ValueError):
                locate_stream(self.image, 1)

    def test_refuses_bad_fixups_and_mft_coverage(self):
        image = bytearray(self.image_bytes(make_resident_attribute(0x80, b"test")))
        image[3072 + 510] ^= 1
        self.image.write_bytes(image)
        with self.assertRaises(ValueError):
            locate_stream(self.image, 1)
        self.image_bytes(make_resident_attribute(0x80, b"test"))
        for number in (-1, 4, 1000):
            with self.assertRaises(ValueError):
                locate_stream(self.image, number)

    def test_refuses_fragmented_mft_instead_of_guessing_record_offset(self):
        self.image_bytes(make_resident_attribute(0x80, b"test"),
                         mft_mapping=b"\x11\x04\x04\x11\x04\x1a\x00")
        with self.assertRaisesRegex(ValueError, "Fragmented"):
            locate_stream(self.image, 1)

    def test_refuses_truncated_image_and_invalid_geometry(self):
        original = self.image_bytes(make_resident_attribute(0x80, b"test"))
        self.image.write_bytes(original[:-1])
        with self.assertRaises(ValueError):
            locate_stream(self.image, 1)
        invalid = bytearray(original)
        invalid[0x0D] = 3
        self.image.write_bytes(invalid)
        with self.assertRaises(ValueError):
            locate_stream(self.image, 1)

    def test_detects_truncation_after_location(self):
        self.image_bytes(nonresident())
        location = locate_stream(self.image, 1)
        self.image.write_bytes(self.image.read_bytes()[:4096])
        with self.assertRaisesRegex(ValueError, "truncated"):
            list(iter_stream_content(location))

    def test_empty_resident_stream_exports_empty_file(self):
        self.image_bytes(make_resident_attribute(0x80, b""))
        result = recover_stream(locate_stream(self.image, 1), self.root / "empty")
        self.assertEqual(result["recovered_length"], 0)
        self.assertEqual((self.root / "empty").read_bytes(), b"")

    def report_run(self, *, stem="report", **expectations):
        return recover_with_report(self.image, 1, "", self.root / f"{stem}.bin",
                                   self.root / f"{stem}.json", **expectations)

    def test_report_pass_contains_source_hashes_expectations_and_actual_results(self):
        original = self.image_bytes(make_resident_attribute(0x80, b"test"))
        digest = hashlib.sha256(b"test").hexdigest()
        source_hash = hashlib.sha256(original).hexdigest()
        result = self.report_run(expected_length=4, expected_sha256=digest,
                                 expected_image_sha256=source_hash)
        saved = json.loads((self.root / "report.json").read_text())
        self.assertEqual(saved, result)
        self.assertEqual(saved["overall_result"], "PASS")
        self.assertTrue(saved["length_match"] and saved["hash_match"])
        self.assertTrue(saved["source_unchanged"] and saved["source_image_hash_match"])
        self.assertEqual(saved["source_sha256_before"], source_hash.upper())
        self.assertEqual(saved["source_sha256_after"], source_hash.upper())
        self.assertEqual(self.image.read_bytes(), original)

    def test_report_mismatched_length_or_hash_is_saved_as_fail(self):
        self.image_bytes(make_resident_attribute(0x80, b"test"))
        digest = hashlib.sha256(b"test").hexdigest()
        for index, expectations in enumerate((
                {"expected_length": 5, "expected_sha256": digest},
                {"expected_length": 4, "expected_sha256": "0" * 64},
                {"expected_length": 5, "expected_sha256": "0" * 64})):
            with self.subTest(expectations=expectations):
                result = self.report_run(stem=f"mismatch{index}", **expectations)
                self.assertEqual(result["overall_result"], "FAIL")
                self.assertEqual((self.root / f"mismatch{index}.bin").read_bytes(), b"test")
                saved = json.loads((self.root / f"mismatch{index}.json").read_text())
                self.assertEqual(saved["overall_result"], "FAIL")

    def test_report_without_both_original_expectations_is_not_verified(self):
        self.image_bytes(make_resident_attribute(0x80, b"test"))
        for index, expectations in enumerate(({}, {"expected_length": 4},
                {"expected_sha256": hashlib.sha256(b"test").hexdigest()})):
            result = self.report_run(stem=f"unverified{index}", **expectations)
            self.assertEqual(result["overall_result"], "NOT_VERIFIED")

    def test_report_preflight_refuses_existing_paths_and_collisions_without_writes(self):
        original = self.image_bytes(make_resident_attribute(0x80, b"test"))
        existing = self.root / "keep.json"
        existing.write_bytes(b"keep")
        new_output, new_report = self.root / "new.bin", self.root / "new.json"
        for output, report in ((existing, new_report), (new_output, existing),
                (self.image, new_report), (new_output, self.image), (new_output, new_output)):
            with self.subTest(output=output, report=report):
                with self.assertRaises(ValueError):
                    recover_with_report(self.image, 1, "", output, report)
                self.assertFalse(new_output.exists())
                self.assertFalse(new_report.exists())
                self.assertEqual(self.image.read_bytes(), original)
                self.assertEqual(existing.read_bytes(), b"keep")

    def test_report_invalid_expectations_do_not_create_files(self):
        self.image_bytes(make_resident_attribute(0x80, b"test"))
        for expectations in ({"expected_length": -1}, {"expected_length": True},
                {"expected_sha256": "bad"}, {"expected_sha256": "Z" * 64},
                {"expected_image_sha256": "bad"}):
            with self.assertRaises(ValueError):
                self.report_run(**expectations)
        self.assertFalse((self.root / "report.bin").exists())
        self.assertFalse((self.root / "report.json").exists())

    def test_report_source_hash_mismatch_refuses_export(self):
        self.image_bytes(make_resident_attribute(0x80, b"test"))
        with self.assertRaisesRegex(ValueError, "Source image hash"):
            self.report_run(expected_image_sha256="0" * 64)
        self.assertFalse((self.root / "report.bin").exists())
        self.assertFalse((self.root / "report.json").exists())

    def test_report_changed_source_hash_is_fail_even_when_payload_matches(self):
        self.image_bytes(make_resident_attribute(0x80, b"test"))
        with patch("ntfs_recovery._sha256_file", side_effect=["A" * 64, "B" * 64]):
            result = self.report_run(expected_length=4,
                                     expected_sha256=hashlib.sha256(b"test").hexdigest())
        self.assertFalse(result["source_unchanged"])
        self.assertTrue(result["hash_match"])
        self.assertEqual(result["overall_result"], "FAIL")

    def test_report_records_recovery_error_without_a_pass_claim(self):
        self.image_bytes(make_resident_attribute(0x80, b"test"))
        with patch("ntfs_recovery.recover_stream", side_effect=ValueError("Read failed")):
            with self.assertRaisesRegex(ValueError, "Read failed"):
                self.report_run()
        saved = json.loads((self.root / "report.json").read_text())
        self.assertEqual(saved["overall_result"], "ERROR")
        self.assertEqual(saved["errors"], ["Read failed"])
        self.assertIsNone(saved["recovered_sha256"])

    def test_report_missing_stream_creates_no_output(self):
        self.image_bytes(make_resident_attribute(0x80, b"test"))
        with self.assertRaises(ValueError):
            recover_with_report(self.image, 1, "Missing", self.root / "out", self.root / "report")
        self.assertFalse((self.root / "out").exists())
        self.assertFalse((self.root / "report").exists())

    def test_report_cli_pass_fail_and_unverified_exit_codes(self):
        self.image_bytes(make_resident_attribute(0x80, b"test"))
        script = Path(__file__).resolve().parents[1] / "code" / "ntfs_recovery.py"
        digest = hashlib.sha256(b"test").hexdigest()
        cases = [("PASS", 0, ["--expected-length", "4", "--expected-sha256", digest]),
                 ("FAIL", 1, ["--expected-length", "4", "--expected-sha256", "0" * 64]),
                 ("NOT_VERIFIED", 1, [])]
        for name, code, flags in cases:
            result = subprocess.run([sys.executable, str(script), str(self.image),
                "--record", "1", "--output", str(self.root / f"{name}.bin"),
                "--report", str(self.root / f"{name}.json"), *flags],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, code, result.stderr)
            self.assertEqual(json.loads(result.stdout)["overall_result"], name)

    def test_report_cli_rejects_missing_output_or_unused_expectations(self):
        self.image_bytes(make_resident_attribute(0x80, b"test"))
        script = Path(__file__).resolve().parents[1] / "code" / "ntfs_recovery.py"
        for flags in (["--report", str(self.root / "report.json")],
                      ["--expected-length", "4"]):
            result = subprocess.run([sys.executable, str(script), str(self.image),
                "--record", "1", *flags], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertFalse((self.root / "report.json").exists())


if __name__ == "__main__":
    unittest.main()
