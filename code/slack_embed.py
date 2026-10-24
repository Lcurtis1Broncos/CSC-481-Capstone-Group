"""Embed a controlled marker in a new copy of the team's verified lab image."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

from ntfs_image_reader import (
    ATTRIBUTE_TYPE_DATA, calculate_absolute_mft_byte_offset,
    calculate_file_slack, decode_data_runs, find_windows_data_partition,
    get_mft_record_offset, parse_file_name_attribute, parse_mbr_partitions,
    parse_mft_attributes, parse_mft_record_header, parse_ntfs_boot_sector,
    read_first_sector, read_mft_record, read_sector_at_offset, restore_record_fixups,
)

LAB_IMAGE_SHA256 = "2240CF8A1AA9D30231C39C4672DC51157093314950C4930EBBF5D30F5F59D2F5"
CHUNK_SIZE = 8 * 1024 * 1024


def locate_lab_slack(source: Path, record_number: int) -> dict:
    """Find final-cluster slack for an ordinary file in the controlled image."""
    sector = read_first_sector(source)
    partition = find_windows_data_partition(parse_mbr_partitions(sector))
    if partition is None:
        raise ValueError("Expected the controlled lab image's MBR data partition.")
    partition_offset = int(partition["byte_offset"])
    boot = parse_ntfs_boot_sector(read_sector_at_offset(source, partition_offset))
    if not boot["ntfs_signature_valid"] or not boot["boot_signature_valid"]:
        raise ValueError("Invalid NTFS boot sector.")
    cluster_size = int(boot["bytes_per_cluster"])
    mft_offset = calculate_absolute_mft_byte_offset(boot, partition_offset)
    record = read_mft_record(source, get_mft_record_offset(
        mft_offset, int(boot["mft_record_size"]), record_number
    ), int(boot["mft_record_size"]))
    header = parse_mft_record_header(record)
    if not header["signature_valid"] or not header["in_use"] or header["is_directory"]:
        raise ValueError("Choose an in-use file record with a valid FILE signature.")
    attributes = parse_mft_attributes(restore_record_fixups(record, int(boot["bytes_per_sector"])))
    if any(a["type"] == 0x20 for a in attributes):
        raise ValueError("Attribute-list extension records are not supported for embedding.")
    streams = [a for a in attributes if a["type"] == ATTRIBUTE_TYPE_DATA and not a["name"]]
    if len(streams) != 1:
        raise ValueError("Expected exactly one unnamed data attribute.")
    data = streams[0]
    if not data["non_resident"]:
        raise ValueError("Resident data has no cluster slack.")
    if int(data["flags"]) & 0xC001 or int(data["start_vcn"]) != 0:
        raise ValueError("Compressed, sparse, encrypted, and extension data are unsupported.")
    runs = decode_data_runs(data["data_runs"])
    volume_clusters = int(boot["total_sectors"]) // int(boot["sectors_per_cluster"])
    for run in runs:
        lcn = run["start_lcn"]
        if lcn is None or lcn + int(run["cluster_count"]) > volume_clusters:
            raise ValueError("Run is sparse or outside the NTFS volume.")
    slack = calculate_file_slack(runs, int(data["real_size"]), cluster_size, partition_offset)
    if slack is None:
        raise ValueError("This file has no final-cluster slack.")
    if slack["byte_offset"] + slack["length"] > source.stat().st_size:
        raise ValueError("Slack range exceeds the image.")
    names = [parse_file_name_attribute(a)["name"] for a in attributes if a["type"] == 0x30]
    return {
        "record_number": record_number, "host_file": names[0] if names else "unknown",
        "logical_size": int(data["real_size"]), "allocated_size": int(data["allocated_size"]),
        "cluster_size": cluster_size, "data_runs": runs, **slack,
    }


def write_working_copy(source: Path, destination: Path, offset: int, payload: bytes) -> dict:
    """Copy, verify the known source hash, patch, and compare every output byte.

    Never opens the source for writing or replaces an existing destination.
    A failed operation may leave a partial copy for inspection.
    """
    source, destination = source.resolve(), destination.resolve()
    if not source.is_file() or source.suffix.lower() != ".dd":
        raise ValueError("Source must be a regular .dd image file.")
    if source == destination or destination.exists():
        raise ValueError("Destination must be a new image path, distinct from the source.")
    if destination.suffix.lower() != ".dd":
        raise ValueError("Destination must use the .dd extension.")
    if not payload or offset < 0 or offset + len(payload) > source.stat().st_size:
        raise ValueError("Invalid payload byte range.")
    if shutil.disk_usage(destination.parent).free < source.stat().st_size + CHUNK_SIZE:
        raise ValueError("Not enough free space for a complete working copy.")
    source_hash = hashlib.sha256()
    with source.open("rb") as original, destination.open("xb") as working:
        while chunk := original.read(CHUNK_SIZE):
            source_hash.update(chunk)
            working.write(chunk)
    if source_hash.hexdigest().upper() != LAB_IMAGE_SHA256:
        raise ValueError("Source hash is not the team's verified ADS lab image; copy left unmodified.")
    with destination.open("r+b") as working:
        working.seek(offset)
        original_slack = working.read(len(payload))
        working.seek(offset)
        working.write(payload)
    image_hash = hashlib.sha256()
    verified_source_hash = hashlib.sha256()
    position = 0
    with source.open("rb") as original, destination.open("rb") as working:
        while chunk := original.read(CHUNK_SIZE):
            verified_source_hash.update(chunk)
            expected = bytearray(chunk)
            low = max(position, offset)
            high = min(position + len(chunk), offset + len(payload))
            if low < high:
                expected[low - position : high - position] = payload[low - offset : high - offset]
            actual = working.read(len(chunk))
            if actual != expected:
                raise ValueError("Working-copy verification failed.")
            image_hash.update(actual)
            position += len(chunk)
        if working.read(1):
            raise ValueError("Working image length changed.")
    if verified_source_hash.digest() != source_hash.digest():
        raise ValueError("Source changed during the operation.")
    return {
        "source_sha256": source_hash.hexdigest().upper(),
        "working_image_sha256": image_hash.hexdigest().upper(),
        "payload_sha256": hashlib.sha256(payload).hexdigest().upper(),
        "payload_length": len(payload), "original_slack_bytes_hex": original_slack.hex(),
        "verification": "Every output byte matches the source except the designated payload range.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--record", type=int, required=True)
    parser.add_argument("--marker", required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.manifest.exists():
            raise ValueError("Manifest already exists; choose a new path.")
        payload = args.marker.encode("utf-8")
        plan = locate_lab_slack(args.source, args.record)
        if len(payload) > plan["length"] or not payload:
            raise ValueError("Payload must fit inside the final-cluster slack.")
        print(f"Host: {plan['host_file']} (MFT record {args.record})", flush=True)
        print(f"Slack offset: {plan['byte_offset']}; available: {plan['length']} bytes", flush=True)
        print("Copying the image, embedding the marker, and verifying all bytes...", flush=True)
        hashes = write_working_copy(args.source, args.destination, plan["byte_offset"], payload)
        manifest = {
            "created_utc": datetime.now(UTC).isoformat(),
            "source_image": args.source.name, "working_image": args.destination.name,
            "marker": args.marker, "encoding": "UTF-8, no BOM or newline",
            **plan, **hashes,
        }
        with args.manifest.open("x", encoding="utf-8") as document:
            json.dump(manifest, document, indent=2)
            document.write("\n")
        print(json.dumps(manifest, indent=2))
        print(f"Manifest saved: {args.manifest}")
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
