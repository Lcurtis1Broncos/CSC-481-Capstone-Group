"""Release dataset tests, independent of the private VirtualBox images."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from generate_submission_dataset import generate
from verify_submission import verify


class SubmissionDatasetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_generated_image_and_manifest_are_deterministic(self):
        first = generate(self.root / "first")
        second = generate(self.root / "second")
        self.assertEqual(first, second)
        self.assertEqual(first["image_bytes"], 32768)
        self.assertEqual((self.root / "first/synthetic.dd").read_bytes(),
                         (self.root / "second/synthetic.dd").read_bytes())

    def test_generator_refuses_existing_directory_without_changes(self):
        generate(self.root / "existing")
        original = (self.root / "existing/synthetic.dd").read_bytes()
        with self.assertRaises(FileExistsError):
            generate(self.root / "existing")
        self.assertEqual((self.root / "existing/synthetic.dd").read_bytes(), original)

    def test_acceptance_workflow_verifies_originals_and_safety(self):
        result = verify(self.root / "acceptance")
        self.assertEqual(result["overall_result"], "PASS")
        self.assertEqual(len(result["checks"]), 7)
        self.assertTrue(result["source_image_unchanged"])

    def test_acceptance_cli_runs_from_an_unrelated_directory(self):
        script = Path(__file__).resolve().parent / "verify_submission.py"
        result = subprocess.run([sys.executable, str(script), str(self.root / "CLI results")],
                                cwd=self.root, capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["overall_result"], "PASS")


if __name__ == "__main__":
    unittest.main()
