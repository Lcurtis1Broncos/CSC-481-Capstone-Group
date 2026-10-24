"""Run the Week 10 controlled-image recovery checks; save actual results.

Not a unit test: requires the team's local working .dd image. Recovered files
are written to a NEW folder; the image is only ever opened read-only.
"""

import argparse
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from ntfs_recovery import locate_stream, recover_stream

EXPECTED_IMAGE = "D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7"
EXPECTED_ADS = "E3CB29B996899849E804A8FD7DB33F7CCECBCB2569005353BD082D320D0D997E"
FILES = [(38, "Test.txt", 83), (39, "Test2.txt", 1778),
         (41, "Testfile.docx", 13437), (42, "SunflowerTest.jpg", 48647),
         (43, "Thetestfile.pdf", 17247), (44, "WaterfallTest.png", 277325),
         (55, "HTMLtestdoc.html", 608), (56, "JSON_test_File.json", 579)]


def image_hash(image):
    with image.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest().upper()


def validate(image, output_directory, report_path):
    if output_directory.exists() or report_path.exists():
        raise ValueError("Choose a NEW recovery directory and report path; nothing is overwritten.")
    print("Verifying the source image before recovery...", flush=True)
    before = image_hash(image)
    if before != EXPECTED_IMAGE:
        raise ValueError("This validation requires the team's recorded ADS/slack working image.")
    output_directory.mkdir(parents=True)
    results = []
    for number, filename, size in FILES:
        location = locate_stream(image, number)
        if location.filename != filename or location.logical_size != size:
            raise ValueError(f"Record {number} disagrees with the eight-file manifest.")
        result = recover_stream(location, output_directory / filename)
        if result["recovered_length"] != size:
            raise ValueError(f"Record {number} recovered length mismatch.")
        result["expected_length"] = size
        result["length_match"] = True
        result["original_content_hash_match"] = None
        results.append(result)
        print(f"Record {number}: {filename}: {size} bytes recovered; size PASS", flush=True)
    ads = recover_stream(locate_stream(image, 58, "CapstoneEvidence"),
                         output_directory / "hostfile_CapstoneEvidence.bin")
    ads["expected_length"] = 36
    ads["expected_sha256"] = EXPECTED_ADS
    ads["length_match"] = ads["recovered_length"] == 36
    ads["hash_match"] = ads["recovered_sha256"] == EXPECTED_ADS
    if not ads["length_match"] or not ads["hash_match"]:
        raise ValueError("Recovered ADS does not match the payload manifest.")
    slack = locate_stream(image, 41).slack
    if slack != {"final_lcn": 3662, "byte_offset": 16049277, "length": 2947}:
        raise ValueError("Slack location differs from the existing slack manifest.")
    print("ADS: 36 bytes; original payload SHA-256 PASS", flush=True)
    print("Slack: offset 16049277, length 2947; manifest range PASS", flush=True)
    print("Verifying the image is unchanged after recovery...", flush=True)
    after = image_hash(image)
    if before != after:
        raise ValueError("Source image changed during validation.")
    report = {
        "test_id": "W10-RECOVERY-SUPPORT", "run_utc": datetime.now(UTC).isoformat(),
        "source_image": image.name, "source_sha256_before": before,
        "source_sha256_after": after, "source_unchanged": True,
        "files": results, "ads": ads, "slack_range": slack,
        "result": "PASS for size, ADS payload hash, slack range, and source preservation checks",
        "limitations": [
            "Original content hashes for the eight baseline files were not supplied; hash equality is unverified.",
            "Actual output hashes are recorded, not presented as independent original-file matches.",
            "Slack bytes are not recovered by this test; only the documented range is checked.",
            "Real-image offset results require independent offset review; synthetic tests check exact known offsets.",
        ],
    }
    with report_path.open("x", encoding="utf-8") as output:
        json.dump(report, output, indent=2)
        output.write("\n")
    print(f"PASS. Report saved: {report_path}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    try:
        validate(args.image, args.output_directory, args.report)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
