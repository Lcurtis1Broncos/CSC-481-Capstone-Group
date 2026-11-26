"""Reproduce the final report's 50 synthetic slack-payload experiments.

Inputs are newly generated parser fixtures, not Windows-created disk images.
Each sample has an independent original; a single-bit change tests verification
failure, not resistance to filesystem copying or forensic detection.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import random
import sys
import time

from generate_submission_dataset import generate

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from ntfs_recovery import recover_with_report


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def campaign(directory):
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=False)
    generate(directory / "fixture")
    base = (directory / "fixture/synthetic.dd").read_bytes()
    rng = random.Random(4812026)
    rows = []
    for number in range(1, 51):
        size = (1, 25, 100, 200, 324)[(number - 1) % 5]
        original = bytes(rng.getrandbits(8) for _ in range(size))
        sample = directory / f"sample_{number:02d}"
        sample.mkdir()
        (sample / "original.bin").write_bytes(original)
        source = bytearray(base)
        source[15548:15548 + size] = original
        image = sample / "source.dd"
        image.write_bytes(source)
        expected_image = sha(source)
        before = time.perf_counter()
        with image.open("rb") as reader:
            reader.seek(15548)
            baseline = reader.read(size)
        baseline_ms = 1000 * (time.perf_counter() - before)
        before = time.perf_counter()
        result = recover_with_report(image, 1, "", sample / "recovered.bin",
            sample / "report.json", expected_length=size,
            expected_sha256=sha(original), expected_image_sha256=expected_image,
            slack_length=size)
        recovery_ms = 1000 * (time.perf_counter() - before)
        recovered = (sample / "recovered.bin").read_bytes()
        assert recovered == original == baseline
        assert result["overall_result"] == "PASS" and result["source_unchanged"]
        # Alter one stored bit in a NEW image and retain the original expectation.
        source[15548] ^= 1
        changed = sample / "one_bit_changed.dd"
        changed.write_bytes(source)
        negative = recover_with_report(changed, 1, "", sample / "changed.bin",
            sample / "changed_report.json", expected_length=size,
            expected_sha256=sha(original), expected_image_sha256=sha(source),
            slack_length=size)
        actual = (sample / "changed.bin").read_bytes()
        bit_errors = sum((a ^ b).bit_count() for a, b in zip(original, actual))
        assert bit_errors == 1 and negative["overall_result"] == "FAIL"
        rows.append(dict(sample=number, payload_bytes=size, available_slack_bytes=324,
            occupancy_percent=100 * size / 324, baseline_exact=True,
            recovered_exact=True, clean_ber_percent=0,
            changed_bits=bit_errors, changed_ber_percent=100 * bit_errors / (8 * size),
            changed_verification="FAIL", source_unchanged=result["source_unchanged"],
            baseline_ms=round(baseline_ms, 6), recovery_report_ms=round(recovery_ms, 6)))
    with (directory / "results.csv").open("x", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = dict(samples=50, dataset="Synthetic NTFS-shaped fixtures",
        payload_sizes=[1, 25, 100, 200, 324], samples_per_size=10,
        clean_exact_matches=50, baseline_exact_matches=50,
        one_bit_changes_detected=50, clean_bit_error_rate_percent=0,
        security_scope="Payload-integrity mismatch detection only; no steganalysis accuracy or detection-evasion experiment",
        python=platform.python_version(), platform=platform.platform(),
        seed=4812026, slack_offset=15548, slack_capacity_bytes=324,
        baseline="Direct byte read at construction-known offset; no metadata parsing",
        timing_scope="Single in-process runs on tiny cached fixtures; not disk throughput benchmarks")
    (directory / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="NEW experiment directory")
    print(json.dumps(campaign(parser.parse_args().directory), indent=2))
