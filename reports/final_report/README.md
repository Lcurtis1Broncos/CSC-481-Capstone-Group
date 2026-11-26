# Final Report

The report follows the instructor-provided LaTeX template: 12-point,
single-column, US Letter, 1-inch margins, and 1.5 line spacing. Its seven
chapters are followed by references and reproducibility/development appendices.
Lucas's earlier Markdown draft remains preserved in `reports/FINAL_TECHNICAL_REPORT.md`.

## Signed Report — Updated November 26

The supplied signed PDF is preserved locally without alteration as
`signed_prior_version_received_2026-11-25.pdf` (excluded from Git).
Both handwritten signatures are visible on PDF page 2; the date fields are
blank. This copy has 50 pages and predates the detection-evasion experiment.

[The signed and dated current report](../NTFS_Filesystem_Steganography_and_Forensic_MFT_Parser_final_report.pdf) has 59 total pages, including
35 chapter pages, and includes the 100-image detection results and expanded
73-test evidence. At Jeff's explicit request on November 26, the signed
declaration page was copied from the earlier report into PDF page 2 of the
current report. The declaration text is identical; all other report text is
preserved. Both signatures are visible. At Jeff's request, both date fields
were filled with November 26, 2026 (`11/26/2026`).
This records a copied handwritten signature page, not a verified digital
signature. The original signed archive and intermediate signature-assembly
copies remain local, excluded from Git. The [unsigned build](main.pdf) is
preserved with the source. Review the assembled report before submission.

## Build

From this folder, run `pdflatex main.tex` repeatedly until references and lists
settle, or run `tectonic main.tex`. Figures are already included under `assets/`.
The source also reads the recorded evidence files under `reports/evidence/`.
Build from a complete repository checkout so these relative paths resolve.

The included `plot_results.py` rebuilds the three result charts from the raw CSV
when Matplotlib is available. Figure preparation used Matplotlib 3.11.2 with
Python 3.12.14. Matplotlib is optional for report figure regeneration and is
not a dependency of the forensic tool or experiment campaign.

`main.pdf` is the unsigned compiled report. The project-named PDF in the
parent `reports/` folder is the current signed and dated submission copy.
Rebuilding the source does not update the signed submission copy.
Both student IDs are supplied. The requested
letter self-assessments are recorded as Lucas A (95/100) and Jeff B (85/100),
using representative numeric values to satisfy the required 0–100 format.
These values represent self-evaluations, not verified current course grades.

## Requirement Review

| Requirement | Location or status |
|---|---|
| 25–35 report pages | The seven chapters occupy 35 pages; front matter and back matter are separate. |
| Seven chapters in order | Chapters 1–7. |
| Abstract no more than 300 words | Front matter; quantitative findings included. |
| 15–20 references | 20 cited primary/official sources with numeric references. |
| Three or four related tools and gap analysis | Chapter 2: Streams, Sleuth Kit, Autopsy, PhotoRec. |
| Architecture, algorithms, formulas, security model | Chapter 3. |
| Environment, call graph, three core code excerpts, challenges | Chapter 4. Historical guest build/VirtualBox/RAM configuration is unavailable and disclosed. |
| Dataset, graphs, tables, measured baseline | Chapter 5; 50 synthetic samples, paired bit-change controls, direct-read baseline. |
| Capacity | Bytes, bits, and slack occupancy; not image bits per pixel. |
| Imperceptibility | PSNR is not applicable to NTFS storage. Byte preservation is discussed separately. |
| Robustness | Measured BER for a single-bit change only; no real-filesystem transformation campaign. |
| Detection evasion | Completed November 25: 100 labeled synthetic images, two fixed rules, confusion counts, accuracy, detection, false-positive and evasion rates; Chapters 3–5 and `../evidence/final_detection/`. General real-volume discovery remains unvalidated. |
| At least three attacks and hardening | Chapter 6. |
| Ethical-use statement | Chapter 1. |
| Self-evaluation | Chapter 7: Jeff B (85/100), Lucas A (95/100), with contribution-based justifications. |
| Quick start, raw results, development logs | Appendices A–C. |
| Originality declaration and signatures | Both handwritten signatures appear on PDF page 2 of the project-named final report, copied at Jeff's request November 26. Both date fields read `11/26/2026`. |
| Student IDs, supervisor, date | Both IDs supplied. Supervisor and November 29 submission date use stated assumptions awaiting correction. |

The professor's metric list includes requirements tailored to other carriers.
The report explains the NTFS-specific adaptations and clearly states where
experiments were not performed. Do not claim strict completion of every
requested metric without the instructor accepting those adaptations or
additional evidence. The detection experiment now supplies the previously
missing measurement within its stated synthetic, known-record scope.

All eight baseline-file original/recovered hash comparisons were confirmed
by Jeff on November 25. The [dated record](../../docs/baseline_hash_verification.md)
states the provenance of that confirmation. Historical logs retain their
earlier unverified status; synthetic results remain separate.

## Evidence and Release Identity

Historical Windows evidence is dated November 15. Release checks are dated
November 24 and recorded under `reports/evidence/final_code/`. The added
50-sample campaign is reproducible with `tests/run_report_campaign.py`; its
CSV and summary are under `reports/evidence/final_report/`. Synthetic data
are explicitly distinguished from Windows-created evidence.

The separate November 25 detection campaign uses 100 images and is reproducible
with `tests/run_detection_campaign.py`. Its evidence is under
`reports/evidence/final_detection/`. Both Windows known-positive checks passed
with the full source-image hash unchanged. The current report-branch suite
passed 73 tests; the tagged release remains the dated 68-test result.

The code tag `v1.0-final` remains at commit `06eb0ff`; report additions do not
move it. GitHub publication of the signed copy does not establish course-site
submission or delivery of the presentation.
The university plagiarism check has not
been performed here.
