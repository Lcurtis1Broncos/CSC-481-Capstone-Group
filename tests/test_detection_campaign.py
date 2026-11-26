"""Check screening boundaries and metric definitions, not stealth guarantees."""
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

from generate_submission_dataset import generate, SLACK
from run_detection_campaign import build_case, named_stream_screen, slack_marker_screen, metrics


class DetectionCampaignTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        generate(self.root / "fixture")
        self.base = (self.root / "fixture/synthetic.dd").read_bytes()

    def source(self, technique, scenario):
        content, label = build_case(self.base, random.Random(123), technique, scenario, 1)
        image = self.root / f"{scenario}.dd"
        image.write_bytes(content)
        return image, label

    def test_named_stream_rule_also_flags_legitimate_streams(self):
        for scenario, flag, label in [("hidden_named_stream", True, True),
                                     ("benign_named_stream", True, False),
                                     ("ordinary_file", False, False)]:
            image, actual_label = self.source("ADS", scenario)
            before = image.read_bytes()
            self.assertEqual(named_stream_screen(image, 2)["flagged"], flag)
            self.assertEqual(actual_label, label)
            self.assertEqual(image.read_bytes(), before)

    def test_slack_rule_respects_location_and_literal_signature(self):
        for scenario, flag in [("plaintext_marker", True), ("xor_marker", False),
                               ("random_slack", False), ("marker_in_logical_content", False)]:
            image, _ = self.source("SLACK", scenario)
            self.assertEqual(slack_marker_screen(image, 1)["flagged"], flag)
        with self.assertRaises(ValueError):
            slack_marker_screen(image, 1, b"")

    def test_metrics_use_negative_and_positive_denominators(self):
        result = metrics([{"outcome": x} for x in ["TP", "TN", "TN", "FP", "FN"]])
        self.assertEqual(result["accuracy_percent"], 60)
        self.assertAlmostEqual(result["false_positive_rate_percent"], 100 / 3)
        self.assertEqual(result["evasion_rate_percent"], 50)
        self.assertIsNone(metrics([])["accuracy_percent"])
        self.assertIsNone(metrics([{"outcome": "TN"}])["evasion_rate_percent"])

    def test_invalid_record_is_an_error_not_a_negative_detection(self):
        image, _ = self.source("ADS", "ordinary_file")
        content = bytearray(image.read_bytes())
        content[4096:4100] = b"BAD!"
        image.write_bytes(content)
        with self.assertRaises(ValueError):
            named_stream_screen(image, 2)

    def test_campaign_cli_accepts_space_in_new_path_and_refuses_reuse(self):
        script = Path(__file__).resolve().parent / "run_detection_campaign.py"
        folder = self.root / "screening results"
        first = subprocess.run([sys.executable, str(script), str(folder)], cwd=self.root,
                               capture_output=True, text=True, timeout=60)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(len((folder / "results.csv").read_text().splitlines()), 101)
        original = (folder / "summary.json").read_bytes()
        again = subprocess.run([sys.executable, str(script), str(folder)], cwd=self.root,
                               capture_output=True, text=True, timeout=60)
        self.assertNotEqual(again.returncode, 0)
        self.assertEqual((folder / "summary.json").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
