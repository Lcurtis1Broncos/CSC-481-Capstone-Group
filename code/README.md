# Source Code

Place all project source code in this folder. Commit working code at least weekly.

## Current tool

`ntfs_image_reader.py` reads the NTFS boot sector and first MFT record from a
disk image without modifying it. It reports the MFT byte offset and verifies
that the first record begins with the `FILE` signature. Run it from the
repository root with:

```powershell
python code/ntfs_image_reader.py path/to/image.dd
```

Selected record attributes and supported data-run/slack locations can be
inspected with `--show-record 41 --show-record 58`. The reader remains read-only;
general payload extraction is not implemented.

## Controlled lab tools

- `slack_embed.py` creates a protected image copy with a documented slack
  marker; see the [procedure](../docs/controlled_slack_space_procedure.md).
- ADS creation uses Lucas's documented manual PowerShell
  [workflow](../docs/ads_creation_workflow.md).

See [parser design and limitations](../docs/parser_design_and_limitations.md).
