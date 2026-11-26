"""Measure two fixed forensic screening rules on labeled synthetic fixtures.

The detector receives an image and selected record, never the sample label,
payload hash, stream name, or planted slack offset. This is a controlled
triage/signature baseline, not a general steganalysis or malware classifier.
"""

import argparse
import csv
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
import platform
import random

from generate_submission_dataset import generate, filename_attribute, SLACK
from test_ntfs_recovery import disk_record
from test_ntfs_image_reader import make_resident_attribute
from ntfs_recovery import locate_stream, locate_slack_payload, iter_stream_content
from ntfs_image_reader import (
    read_first_sector, parse_ntfs_boot_sector, parse_mbr_partitions,
    find_windows_data_partition, read_sector_at_offset, read_mft_record,
    restore_record_fixups, parse_mft_attributes,
)

SEED = 4811125
SLACK_START = 15548
SLACK_CAPACITY = 324
LAB_HASH = "D54886033D5ED8E6B9BA5C58EF60A414C3F2202BD1A2F6A5A7D407D499BCA5C7"


def file_hash(path):
    with Path(path).open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest().upper()


def named_stream_screen(image, record):
    """Flag ANY named DATA attribute, including legitimate named streams."""
    image = Path(image)
    location = locate_stream(image, record)  # Strict geometry/record validation.
    first = read_first_sector(image)
    boot = parse_ntfs_boot_sector(first)
    if not boot["ntfs_signature_valid"]:
        partition = find_windows_data_partition(parse_mbr_partitions(first))
        if partition is None:
            raise ValueError("No supported Windows data partition.")
        boot = parse_ntfs_boot_sector(read_sector_at_offset(image, int(partition["byte_offset"])))
    raw = read_mft_record(image, location.record_offset, int(boot["mft_record_size"]))
    attributes = parse_mft_attributes(restore_record_fixups(raw, int(boot["bytes_per_sector"])))
    names = [str(a["name"]) for a in attributes if a["type"] == 0x80 and a["name"]]
    return {"flagged": bool(names), "named_streams": names}


def slack_marker_screen(image, record, signature=SLACK):
    """Search the calculated tail, not ordinary content or a supplied offset."""
    if not isinstance(signature, bytes) or not signature:
        raise ValueError("The marker signature must be nonempty bytes.")
    host = locate_stream(Path(image), record)
    if host.slack is None:
        return {"flagged": False, "marker_relative_offset": None}
    selected = locate_slack_payload(Path(image), record, host.slack["length"])
    content = b"".join(iter_stream_content(selected))
    position = content.find(signature)
    return {"flagged": position >= 0,
            "marker_relative_offset": None if position < 0 else position}


def metrics(rows):
    counts = {name: sum(r["outcome"] == name for r in rows) for name in ("TP", "TN", "FP", "FN")}
    positive = counts["TP"] + counts["FN"]
    negative = counts["FP"] + counts["TN"]
    rate = lambda numerator, denominator: None if not denominator else 100 * numerator / denominator
    return {**counts, "samples": len(rows), "positives": positive, "negatives": negative,
            "accuracy_percent": rate(counts["TP"] + counts["TN"], len(rows)),
            "detection_rate_percent": rate(counts["TP"], positive),
            "false_positive_rate_percent": rate(counts["FP"], negative),
            "evasion_rate_percent": rate(counts["FN"], positive)}


def build_case(base, rng, technique, scenario, index):
    """Construct labels independently of the screening functions."""
    image = bytearray(base)
    # Remove both original markers from the shared fixture before each case.
    image[4096:5120] = disk_record(filename_attribute("hostfile.txt"),
                                  make_resident_attribute(0x80, b"X" * 31))
    image[SLACK_START:SLACK_START + SLACK_CAPACITY] = bytes(rng.getrandbits(8) for _ in range(SLACK_CAPACITY))
    if SLACK in image[SLACK_START:SLACK_START + SLACK_CAPACITY]:
        raise ValueError("Unexpected signature in generated control bytes.")
    hidden = scenario in ("hidden_named_stream", "plaintext_marker", "xor_marker")
    if technique == "ADS" and scenario != "ordinary_file":
        name = (f"Research_{index:02d}" if hidden else
                ("Zone.Identifier", "SummaryInformation")[index % 2])
        value = (b"LAB_HIDDEN_" + bytes(rng.getrandbits(8) for _ in range(40 + index % 7))
                 if hidden else b"[ZoneTransfer]\r\nZoneId=3\r\n")
        image[4096:5120] = disk_record(filename_attribute("hostfile.txt"),
            make_resident_attribute(0x80, b"X" * 31),
            make_resident_attribute(0x80, value, name=name))
    elif technique == "SLACK":
        if hidden:
            offset = (index * 37) % (SLACK_CAPACITY - len(SLACK) + 1)
            value = SLACK if scenario == "plaintext_marker" else bytes(b ^ 0x5A for b in SLACK)
            image[SLACK_START + offset:SLACK_START + offset + len(value)] = value
        elif scenario == "marker_in_logical_content":
            image[40 * 512:40 * 512 + len(SLACK)] = SLACK
    return bytes(image), hidden


def campaign(directory, lab_image=None):
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=False)
    generate(directory / "fixture")
    base = (directory / "fixture/synthetic.dd").read_bytes()
    rng = random.Random(SEED)
    rows = []
    manifest = []
    groups = {"ADS": [("hidden_named_stream", 25), ("benign_named_stream", 10), ("ordinary_file", 15)],
              "SLACK": [("plaintext_marker", 15), ("xor_marker", 10),
                        ("random_slack", 15), ("marker_in_logical_content", 10)]}
    for technique, scenarios in groups.items():
        index = 0
        for scenario, count in scenarios:
            for _ in range(count):
                index += 1
                source_bytes, hidden = build_case(base, rng, technique, scenario, index)
                source = directory / f"{technique.lower()}_{index:02d}.dd"
                source.write_bytes(source_bytes)
                before = file_hash(source)
                detected = (named_stream_screen(source, 2) if technique == "ADS" else
                            slack_marker_screen(source, 1))
                unchanged = before == file_hash(source)
                if not unchanged:
                    raise ValueError("Detector changed a source image.")
                flag = detected["flagged"]
                outcome = ("TP" if flag else "FN") if hidden else ("FP" if flag else "TN")
                rows.append({"sample_id": source.stem, "technique": technique, "scenario": scenario,
                             "hidden_payload_present": hidden, "flagged": flag, "outcome": outcome,
                             "source_unchanged": unchanged})
                manifest.append({"image": source.name, "sha256": before, "record": 2 if technique == "ADS" else 1,
                                 "scenario": scenario, "hidden_payload_present": hidden})
    with (directory / "results.csv").open("x", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {"created_utc": datetime.now(UTC).isoformat(), "python": platform.python_version(),
        "seed": SEED, "synthetic_images": len(rows),
        "scope": "Known-record synthetic screening experiment; not population accuracy or general steganalysis",
        "ground_truth": "Intentional hidden payload versus legitimate stream/ordinary-content control, defined at construction",
        "ADS": metrics([r for r in rows if r["technique"] == "ADS"]),
        "SLACK": metrics([r for r in rows if r["technique"] == "SLACK"]),
        "source_images_unchanged": all(r["source_unchanged"] for r in rows),
        "definitions": {"ADS_rule": "Flag any named DATA attribute in selected record",
                        "SLACK_rule": "Find literal TEAM3_SLACK_TEST_20261008 only in calculated slack",
                        "evasion": "Hidden-positive cases not flagged by that fixed screening rule"}}
    if lab_image is not None:
        lab_image = Path(lab_image).resolve()
        before = file_hash(lab_image)
        if before != LAB_HASH:
            raise ValueError("Lab image differs from the recorded working image.")
        ads = named_stream_screen(lab_image, 58)
        slack = slack_marker_screen(lab_image, 41)
        after = file_hash(lab_image)
        if before != after or not ads["flagged"] or not slack["flagged"]:
            raise ValueError("Lab positive check or source preservation failed.")
        summary["windows_lab_positive_check"] = {"ADS": ads, "SLACK": slack,
            "source_sha256_before": before, "source_sha256_after": after,
            "source_unchanged": before == after,
            "scope": "Two known positive records only; no real-volume negative-rate claim"}
    (directory / "fixture_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (directory / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="NEW directory for all experiment inputs and results")
    parser.add_argument("--lab-image", type=Path, help="optional preserved Windows working image")
    args = parser.parse_args()
    try:
        print(json.dumps(campaign(args.directory, args.lab_image), indent=2))
    except (OSError, ValueError) as error:
        parser.error(str(error))
