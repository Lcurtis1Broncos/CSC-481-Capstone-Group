"""Verify the submission end to end using only its generated synthetic data."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from generate_submission_dataset import generate

ROOT = Path(__file__).resolve().parents[1]


def verify(directory: Path):
    directory = directory.resolve()
    # Keep all test artifacts in a NEW folder; never reuse or delete outputs.
    directory.mkdir(parents=True, exist_ok=False)
    manifest = generate(directory / "dataset")
    image = directory / "dataset" / manifest["image"]
    expected_image = manifest["image_sha256"]
    checks = []

    def run(script, arguments, expected_code):
        result = subprocess.run([sys.executable, str(ROOT / "code" / script),
                                 str(image), *map(str, arguments)],
                                capture_output=True, text=True, timeout=60)
        if result.returncode != expected_code:
            raise ValueError(f"{script}: expected exit {expected_code}, got {result.returncode}: {result.stderr}")
        return result

    view = run("ntfs_image_reader.py", ["--list-files", 8, "--show-record", 1,
                                       "--show-record", 2], 0)
    if "CapstoneEvidence" not in view.stdout or "SyntheticHost.bin" not in view.stdout:
        raise ValueError("Parser did not display the known fixture file/ADS.")
    with (directory / "parser_output.txt").open("x", encoding="utf-8") as output:
        output.write(view.stdout)
    checks.append("Parser identifies synthetic file and named ADS")
    for item in manifest["items"]:
        output = directory / (item["name"] + ".bin")
        report = directory / (item["name"] + ".json")
        flags = ["--record", item["record"], "--stream", item["stream"],
                 "--output", output, "--report", report, "--expected-length", item["length"],
                 "--expected-sha256", item["sha256"], "--expected-image-sha256", expected_image]
        if "slack_length" in item:
            flags += ["--slack-length", item["slack_length"]]
        run("ntfs_recovery.py", flags, 0)
        saved = json.loads(report.read_text(encoding="utf-8"))
        if saved["overall_result"] != "PASS" or not saved["source_unchanged"]:
            raise ValueError("Generated recovery report did not pass.")
        if output.read_bytes() != (directory / "dataset" / item["original"]).read_bytes():
            raise ValueError("Recovered bytes differ from the independently generated original.")
        if "image_offset" in item and saved["extents"][0]["image_offset"] != item["image_offset"]:
            raise ValueError("Slack location differs from the constructed fixture.")
        checks.append(f"{item['name']}: exact original bytes/hash and unchanged source")

    negative = run("ntfs_recovery.py", ["--record", 2, "--stream", "CapstoneEvidence",
        "--output", directory / "wrong_hash.bin", "--report", directory / "wrong_hash.json",
        "--expected-length", 36, "--expected-sha256", "0" * 64], 1)
    result = json.loads(negative.stdout)
    if result["overall_result"] != "FAIL" or result["hash_match"] or not result["source_unchanged"]:
        raise ValueError("Wrong expected hash did not produce the required verification failure.")
    checks.append("Wrong original hash gives FAIL and exit 1")

    old_output = (directory / "ads.bin").read_bytes()
    old_report = (directory / "ads.json").read_bytes()
    run("ntfs_recovery.py", ["--record", 2, "--stream", "CapstoneEvidence",
        "--output", directory / "ads.bin", "--report", directory / "ads.json"], 2)
    if (directory / "ads.bin").read_bytes() != old_output or (directory / "ads.json").read_bytes() != old_report:
        raise ValueError("Overwrite refusal did not preserve existing files.")
    checks.append("Existing output and report remain unchanged")

    invalid = run("ntfs_recovery.py", ["--record", 1, "--slack-length", 325,
        "--output", directory / "outside.bin", "--report", directory / "outside.json"], 2)
    if "outside" not in invalid.stderr or (directory / "outside.bin").exists() or (directory / "outside.json").exists():
        raise ValueError("Invalid slack range was not safely refused before file creation.")
    checks.append("Out-of-range slack read creates no files")

    with image.open("rb") as source:
        actual_image = hashlib.file_digest(source, "sha256").hexdigest().upper()
    if actual_image != expected_image:
        raise ValueError("Synthetic source image changed during verification.")
    summary = {"overall_result": "PASS", "dataset": manifest["dataset"],
               "checks": checks, "source_image_unchanged": True,
               "scope": "Synthetic acceptance checks; does not verify the eight original VirtualBox files"}
    with (directory / "verification.json").open("x", encoding="utf-8") as document:
        json.dump(summary, document, indent=2)
        document.write("\n")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="NEW directory for all generated inputs/results")
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.directory), indent=2))
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
