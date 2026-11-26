"""Create a small deterministic NTFS-shaped test image in a NEW directory.

This handcrafted fixture is not a Windows-formatted/mountable filesystem or
the original VirtualBox evidence image. It reproduces the supported parser,
fragmented-file, resident ADS, and bounded-slack paths without external data.
"""

import argparse
import hashlib
import json
from pathlib import Path

from test_ntfs_image_reader import make_boot_sector, make_resident_attribute
from test_ntfs_recovery import disk_record, nonresident

ADS = b"CAPSTONE_ADS_TEST_20261001_Team3_001"
SLACK = b"TEAM3_SLACK_TEST_20261008"
HOST = b"A" * 512 + b"B" * 188


def digest(data):
    return hashlib.sha256(data).hexdigest().upper()


def filename_attribute(name):
    encoded = name.encode("utf-16-le")
    value = bytearray(66 + len(encoded))
    value[:8] = (5).to_bytes(8, "little")
    value[64], value[65] = len(name), 1
    value[66:] = encoded
    return make_resident_attribute(0x30, bytes(value))


def generate(directory: Path):
    image = bytearray(64 * 512)
    boot = bytearray(make_boot_sector(bytes_per_sector=512, sectors_per_cluster=1, mft_lcn=4))
    boot[0x28:0x30] = (64).to_bytes(8, "little")
    boot[0x40] = 246  # Signed -10: 1024-byte MFT records.
    image[:512] = boot
    records = {
        0: disk_record(filename_attribute("$MFT"), nonresident(
            size=8192, allocated=8192, mapping=b"\x11\x10\x04\x00", end=15)),
        1: disk_record(filename_attribute("SyntheticHost.bin"), nonresident(
            mapping=b"\x11\x01\x28\x11\x01\xf6\x00")),
        2: disk_record(filename_attribute("hostfile.txt"),
            make_resident_attribute(0x80, b"X" * 31),
            make_resident_attribute(0x80, ADS, name="CapstoneEvidence")),
        3: disk_record(filename_attribute("$Volume"),
            make_resident_attribute(0x60, "SYNTHETIC".encode("utf-16-le"))),
        5: disk_record(filename_attribute("."), flags=3),
    }
    for number, record in records.items():
        start = 2048 + number * 1024
        image[start:start + 1024] = record
    # Two physical fragments in logical order; second run has a negative delta.
    image[40 * 512:41 * 512] = HOST[:512]
    image[30 * 512:30 * 512 + 188] = HOST[512:]
    slack_start = 30 * 512 + 188
    image[slack_start:slack_start + len(SLACK)] = SLACK
    items = [
        {"name": "host", "record": 1, "stream": "", "length": len(HOST),
         "sha256": digest(HOST), "original": "host_original.bin"},
        {"name": "ads", "record": 2, "stream": "CapstoneEvidence", "length": len(ADS),
         "sha256": digest(ADS), "original": "ads_original.bin"},
        {"name": "slack", "record": 1, "stream": "", "length": len(SLACK),
         "sha256": digest(SLACK), "original": "slack_original.bin",
         "slack_length": len(SLACK), "image_offset": slack_start},
    ]
    manifest = {"dataset": "Deterministic synthetic submission fixture",
                "scope": "Handcrafted NTFS-shaped structures; not original lab evidence or a mountable volume",
                "image": "synthetic.dd", "image_bytes": len(image),
                "image_sha256": digest(image), "items": items}
    # Fail before modifying anything if this directory already exists.
    directory.mkdir(parents=True, exist_ok=False)
    for name, data in (("synthetic.dd", image), ("host_original.bin", HOST),
                       ("ads_original.bin", ADS), ("slack_original.bin", SLACK)):
        with (directory / name).open("xb") as output:
            output.write(data)
    with (directory / "manifest.json").open("x", encoding="utf-8") as output:
        json.dump(manifest, output, indent=2)
        output.write("\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="NEW output directory")
    args = parser.parse_args()
    try:
        print(json.dumps(generate(args.directory), indent=2))
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
