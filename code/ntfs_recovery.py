"""Read-only recovery support for ordinary streams in controlled NTFS images.

This is the support layer for the team's extractor, not a general NTFS tool.
MFT extension attributes, sparse/compressed/encrypted streams, and fragmented
$MFT layouts are deliberately refused rather than guessed.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path

from ntfs_image_reader import (
    calculate_absolute_mft_byte_offset, calculate_file_slack,
    cluster_to_image_offset, decode_data_runs, find_windows_data_partition,
    parse_file_name_attribute, parse_mbr_partitions, parse_mft_attributes,
    parse_mft_record_header, parse_ntfs_boot_sector, read_first_sector,
    read_mft_record, read_sector_at_offset, restore_record_fixups,
)

CHUNK_SIZE = 1024 * 1024


@dataclass(frozen=True)
class StreamLocation:
    image: Path
    record_number: int
    record_offset: int
    filename: str
    stream_name: str
    logical_size: int
    initialized_size: int
    resident_value: bytes | None
    # (absolute image offset, allocated byte count), in logical file order.
    extents: tuple[tuple[int, int], ...]
    slack: dict[str, int] | None

    def summary(self) -> dict:
        return {
            "source_image": self.image.name,
            "record_number": self.record_number,
            "record_offset": self.record_offset,
            "host_filename": self.filename,
            "stream_name": self.stream_name,
            "resident": self.resident_value is not None,
            "logical_size": self.logical_size,
            "initialized_size": self.initialized_size,
            "extents": [{"image_offset": offset, "allocated_length": length}
                        for offset, length in self.extents],
            "slack": self.slack,
            "resident_note": (
                "Content comes from the USA-restored MFT record, not a raw contiguous range."
                if self.resident_value is not None else None
            ),
        }


def _attributes(raw: bytes, sector_size: int, *, allow_directory: bool = False) -> list[dict]:
    header = parse_mft_record_header(raw)
    if not header["signature_valid"] or not header["in_use"]:
        raise ValueError("Recovery requires a valid, in-use FILE record.")
    if header["is_directory"] and not allow_directory:
        raise ValueError("Directory content recovery is unsupported.")
    record = restore_record_fixups(raw, sector_size)
    if any(record[0x20:0x28]):
        raise ValueError("Extension records are unsupported.")
    start = int(header["first_attribute_offset"])
    usa_end = int.from_bytes(raw[4:6], "little") + 2 * int.from_bytes(raw[6:8], "little")
    used = int.from_bytes(record[0x18:0x1C], "little")
    if start < max(0x30, usa_end) or start % 8 or not start + 4 <= used <= len(record):
        raise ValueError("Invalid MFT attribute boundaries.")
    position = start
    while position + 4 <= used and record[position:position + 4] != b"\xff" * 4:
        if position + 16 > used:
            raise ValueError("Truncated attribute header.")
        length = int.from_bytes(record[position + 4:position + 8], "little")
        nonresident = record[position + 8]
        minimum = 0x40 if nonresident else 0x18
        if nonresident not in (0, 1) or length < minimum or length % 8 or position + length > used:
            raise ValueError("Invalid attribute header or length.")
        if record[position + 9]:
            name_offset = int.from_bytes(record[position + 10:position + 12], "little")
            if name_offset < minimum:
                raise ValueError("Attribute name overlaps its header.")
        position += length
    attributes = parse_mft_attributes(record[:used])
    end = start + sum(int(a["length"]) for a in attributes)
    if record[end:end + 4] != b"\xff" * 4:
        raise ValueError("MFT attribute list is missing its end marker.")
    if any(a["type"] == 0x20 for a in attributes):
        raise ValueError("$ATTRIBUTE_LIST extensions are unsupported.")
    return attributes


def _select_stream(attributes: list[dict], name: str) -> dict:
    matches = [a for a in attributes if a["type"] == 0x80 and a["name"] == name]
    if len(matches) != 1:
        raise ValueError("Expected exactly one matching $DATA attribute.")
    data = matches[0]
    if int(data["flags"]) & 0xC001:
        raise ValueError("Compressed, encrypted, and sparse streams are unsupported.")
    return data


def _runs(data: dict, boot: dict) -> list[dict]:
    if int(data["start_vcn"]) != 0:
        raise ValueError("A complete base data attribute starting at VCN zero is required.")
    runs = decode_data_runs(data["data_runs"])
    cluster_size = int(boot["bytes_per_cluster"])
    volume_clusters = int(boot["total_sectors"]) // int(boot["sectors_per_cluster"])
    for run in runs:
        lcn = run["start_lcn"]
        if lcn is None or lcn + int(run["cluster_count"]) > volume_clusters:
            raise ValueError("Data run is sparse or outside the NTFS volume.")
    coverage = sum(int(r["cluster_count"]) for r in runs) * cluster_size
    if runs and int(data["end_vcn"]) + 1 != coverage // cluster_size:
        raise ValueError("Ending VCN does not match the data runs.")
    if not 0 <= int(data["initialized_size"]) <= int(data["real_size"]) <= coverage:
        raise ValueError("Data sizes are inconsistent with run coverage.")
    if int(data["allocated_size"]) != coverage:
        raise ValueError("Allocated size does not match the complete data runs.")
    return runs


def locate_stream(image: Path, record_number: int, stream_name: str = "") -> StreamLocation:
    """Locate one stream; validate geometry, USA fixups, MFT coverage and runs."""
    image = image.resolve()
    if record_number < 0:
        raise ValueError("Record number cannot be negative.")
    first = read_first_sector(image)
    boot = parse_ntfs_boot_sector(first)
    partition_offset = 0
    partition = None
    if not boot["ntfs_signature_valid"]:
        if first[510:512] != b"\x55\xaa":
            raise ValueError("Invalid MBR signature.")
        partition = find_windows_data_partition(parse_mbr_partitions(first))
        if partition is None:
            raise ValueError("No MBR Windows data partition found; GPT is unsupported.")
        partition_offset = int(partition["byte_offset"])
        boot = parse_ntfs_boot_sector(read_sector_at_offset(image, partition_offset))
    sector_size = int(boot["bytes_per_sector"])
    cluster_size = int(boot["bytes_per_cluster"])
    record_size = int(boot["mft_record_size"])
    spc = int(boot["sectors_per_cluster"])
    if (not boot["ntfs_signature_valid"] or not boot["boot_signature_valid"]
            or sector_size not in (512, 1024, 2048, 4096)
            or spc < 1 or spc > 128 or spc & (spc - 1)
            or record_size < sector_size or record_size > 65536
            or record_size % sector_size or record_size & (record_size - 1)):
        raise ValueError("Unsupported or invalid NTFS geometry.")
    volume_size = int(boot["total_sectors"]) * sector_size
    if volume_size < cluster_size or partition_offset + volume_size > image.stat().st_size:
        raise ValueError("NTFS volume exceeds the image or has invalid size.")
    if partition and volume_size > int(partition["total_sectors"]) * 512:
        raise ValueError("NTFS volume exceeds its MBR partition.")
    mft_offset = calculate_absolute_mft_byte_offset(boot, partition_offset)
    if not partition_offset <= mft_offset <= partition_offset + volume_size - record_size:
        raise ValueError("MFT record zero is outside the volume.")
    mft_attributes = _attributes(read_mft_record(image, mft_offset, record_size), sector_size)
    mft_data = _select_stream(mft_attributes, "")
    if not mft_data["non_resident"]:
        raise ValueError("Expected a nonresident $MFT data stream.")
    mft_runs = _runs(mft_data, boot)
    if (len(mft_runs) != 1 or mft_runs[0]["start_lcn"] != int(boot["mft_start_lcn"])):
        raise ValueError("Fragmented $MFT layouts are unsupported for recovery.")
    relative = record_number * record_size
    if relative + record_size > int(mft_data["initialized_size"]):
        raise ValueError("Requested record is outside initialized $MFT content.")
    record_offset = mft_offset + relative
    attributes = _attributes(read_mft_record(image, record_offset, record_size), sector_size)
    data = _select_stream(attributes, stream_name)
    names = [str(parse_file_name_attribute(a)["name"])
             for a in attributes if a["type"] == 0x30]
    value = data.get("value") if not data["non_resident"] else None
    extents = ()
    slack = None
    if value is not None:
        logical_size = initialized_size = len(value)
    else:
        runs = _runs(data, boot)
        logical_size = int(data["real_size"])
        initialized_size = int(data["initialized_size"])
        extents = tuple((cluster_to_image_offset(int(r["start_lcn"]), cluster_size,
                                                partition_offset),
                         int(r["cluster_count"]) * cluster_size) for r in runs)
        slack = calculate_file_slack(runs, logical_size, cluster_size, partition_offset)
    return StreamLocation(image, record_number, record_offset,
                          names[0] if names else "[no filename]", stream_name,
                          logical_size, initialized_size, value, extents, slack)


def iter_stream_content(location: StreamLocation):
    """Yield logical content in bounded chunks; never include cluster slack.

    NTFS bytes past initialized size read as zero, not stale disk contents.
    Keep the source image unchanged between locating and recovering a stream.
    """
    if location.resident_value is not None:
        yield location.resident_value
        return
    remaining = location.initialized_size
    with location.image.open("rb") as source:
        for offset, length in location.extents:
            source.seek(offset)
            extent_remaining = min(length, remaining)
            while extent_remaining:
                size = min(CHUNK_SIZE, extent_remaining)
                chunk = source.read(size)
                if len(chunk) != size:
                    raise ValueError("Source was truncated during recovery.")
                yield chunk
                remaining -= size
                extent_remaining -= size
            if not remaining:
                break
    if remaining:
        raise ValueError("Insufficient extents for initialized stream content.")
    remaining = location.logical_size - location.initialized_size
    while remaining:
        size = min(CHUNK_SIZE, remaining)
        yield bytes(size)
        remaining -= size


def recover_stream(location: StreamLocation, destination: Path) -> dict:
    """Export to a NEW file; return actual length/hash for Lucas's report.

    A failure can leave a partial output. It is not a successful recovery;
    choose a new output path before retrying. Never opens the image for writing.
    """
    destination = destination.resolve()
    if destination == location.image or destination.exists():
        raise ValueError("Choose a new destination distinct from the source image.")
    digest = hashlib.sha256()
    count = 0
    with destination.open("xb") as output:
        for chunk in iter_stream_content(location):
            output.write(chunk)
            digest.update(chunk)
            count += len(chunk)
    if count != location.logical_size:
        raise ValueError("Recovered length does not match the logical stream size.")
    return {**location.summary(), "output_filename": destination.name,
            "recovered_length": count, "recovered_sha256": digest.hexdigest().upper()}


def _sha256_file(path: Path) -> str:
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest().upper()


def _expected_hash(value: str | None) -> str | None:
    if value is None:
        return None
    if len(value) != 64 or any(c not in "0123456789abcdefABCDEF" for c in value):
        raise ValueError("Expected SHA-256 must contain exactly 64 hexadecimal characters.")
    return value.upper()


def recover_with_report(
    image: Path, record_number: int, stream_name: str,
    destination: Path, report_path: Path, *,
    expected_length: int | None = None, expected_sha256: str | None = None,
    expected_image_sha256: str | None = None,
) -> dict:
    """Team 3 extractor/report integration using the existing support engine.

    Hashes the input before and after export. PASS requires independent
    expected payload length AND hash; absent expectations are NOT_VERIFIED.
    Mismatched expectations produce a saved FAIL report, not a false success.
    After report reservation, recovery errors produce an ERROR report. Partial
    outputs are retained for inspection; nothing existing is overwritten.
    """
    expected_sha256 = _expected_hash(expected_sha256)
    expected_image_sha256 = _expected_hash(expected_image_sha256)
    if expected_length is not None and (type(expected_length) is not int or expected_length < 0):
        raise ValueError("Expected length must be a nonnegative integer.")
    image, destination, report_path = image.resolve(), destination.resolve(), report_path.resolve()
    if len({image, destination, report_path}) != 3:
        raise ValueError("Image, recovered output, and report must be distinct paths.")
    if destination.exists() or report_path.exists():
        raise ValueError("Output and report must both be NEW files; nothing is overwritten.")
    if not destination.parent.is_dir() or not report_path.parent.is_dir():
        raise ValueError("Output and report parent directories must already exist.")
    location = locate_stream(image, record_number, stream_name)
    before = _sha256_file(image)
    if expected_image_sha256 is not None and before != expected_image_sha256:
        raise ValueError("Source image hash does not match the expected image; export refused.")
    report = {
        "test_id": "TEAM3-STREAM-RECOVERY",
        "team": "CSC-481 Team 3",
        "created_utc": datetime.now(UTC).isoformat(),
        "tool": "ntfs_recovery.py; Week 10 integrated reporting",
        "source_image_path": str(image),
        "source_sha256_before": before,
        "source_sha256_after": None,
        "expected_image_sha256": expected_image_sha256,
        "source_image_hash_match": None if expected_image_sha256 is None else True,
        "source_unchanged": None,
        **location.summary(),
        "output_path": str(destination),
        "expected_length": expected_length,
        "expected_sha256": expected_sha256,
        "recovered_length": None, "recovered_sha256": None,
        "length_match": None, "hash_match": None,
        "overall_result": "ERROR", "errors": [],
    }
    # Exclusive creation also guards against an existing report appearing
    # after preflight. recover_stream independently reserves its output.
    with report_path.open("x", encoding="utf-8") as document:
        try:
            report.update(recover_stream(location, destination))
            report["source_sha256_after"] = _sha256_file(image)
            report["source_unchanged"] = before == report["source_sha256_after"]
            report["length_match"] = (None if expected_length is None else
                                      report["recovered_length"] == expected_length)
            report["hash_match"] = (None if expected_sha256 is None else
                                    report["recovered_sha256"] == expected_sha256)
            checks = (report["length_match"], report["hash_match"])
            if not report["source_unchanged"] or False in checks:
                report["overall_result"] = "FAIL"
            elif None in checks:
                report["overall_result"] = "NOT_VERIFIED"
            else:
                report["overall_result"] = "PASS"
        except (OSError, ValueError) as error:
            report["errors"].append(str(error))
            json.dump(report, document, indent=2)
            document.write("\n")
            raise
        json.dump(report, document, indent=2)
        document.write("\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--record", type=int, required=True)
    parser.add_argument("--stream", default="", help="exact ADS name; omit for unnamed content")
    parser.add_argument("--output", type=Path, help="new output file; omit to locate only")
    parser.add_argument("--report", type=Path, help="save a NEW JSON recovery report; requires --output")
    parser.add_argument("--expected-length", type=int, help="original payload byte count")
    parser.add_argument("--expected-sha256", help="original payload SHA-256 from its manifest")
    parser.add_argument("--expected-image-sha256", help="refuse export if source image differs")
    args = parser.parse_args()
    if args.report is not None and args.output is None:
        parser.error("--report requires --output")
    if args.report is None and any(value is not None for value in (
            args.expected_length, args.expected_sha256, args.expected_image_sha256)):
        parser.error("expected-value comparisons require --report and --output")
    try:
        if args.report is not None:
            result = recover_with_report(
                args.image, args.record, args.stream, args.output, args.report,
                expected_length=args.expected_length, expected_sha256=args.expected_sha256,
                expected_image_sha256=args.expected_image_sha256,
            )
        else:
            location = locate_stream(args.image, args.record, args.stream)
            result = recover_stream(location, args.output) if args.output else location.summary()
        print(json.dumps(result, indent=2))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if result.get("overall_result") in ("FAIL", "NOT_VERIFIED"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
