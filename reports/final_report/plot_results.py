"""Rebuild the report's two measured-result plots (optional Matplotlib)."""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
with (ROOT / "../evidence/final_report/results.csv").open() as source:
    rows = list(csv.DictReader(source))
sizes = sorted({int(row["payload_bytes"]) for row in rows})
first = {size: next(row for row in rows if int(row["payload_bytes"]) == size) for size in sizes}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "axes.titlesize": 13, "axes.labelsize": 11, "pdf.fonttype": 42})

fig, ax = plt.subplots(figsize=(7, 3.4))
values = [float(first[size]["occupancy_percent"]) for size in sizes]
ax.bar([str(size) for size in sizes], values, color="#355c7d", label="Selected / available slack")
ax.set(xlabel="Payload length (bytes)", ylabel="Slack occupancy (%)",
       title="Synthetic slack capacity and selected payloads", ylim=(0, 112))
for index, value in enumerate(values):
    ax.text(index, value + 2, f"{value:.2f}%", ha="center", fontsize=10)
ax.legend(loc="upper left", frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(ROOT / "assets/capacity.pdf", bbox_inches="tight")
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 3.4))
ax.plot(sizes, [float(first[size]["changed_ber_percent"]) for size in sizes],
        "o-", color="#9b3a32", label="One changed bit")
ax.plot(sizes, [float(first[size]["clean_ber_percent"]) for size in sizes],
        "s--", color="#355c7d", label="Unchanged payload")
ax.set(xlabel="Payload length (bytes)", ylabel="Bit error rate (%)",
       title="Payload error after a controlled single-bit change")
ax.legend(frameon=False)
ax.grid(axis="y", alpha=.2)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(ROOT / "assets/ber.pdf", bbox_inches="tight")
plt.close(fig)
with (ROOT / "../evidence/final_detection/summary.json").open() as source:
    detection = json.load(source)
labels = ["Detection", "False positives", "Evasion"]
keys = ["detection_rate_percent", "false_positive_rate_percent", "evasion_rate_percent"]
fig, ax = plt.subplots(figsize=(7, 3.5))
for offset, rule, color, title in [(-.19, "ADS", "#355c7d", "Named-stream screening"),
                                   (.19, "SLACK", "#9b3a32", "Slack marker search")]:
    bars = ax.bar([i + offset for i in range(3)], [detection[rule][k] for k in keys],
                  width=.36, color=color, label=title)
    ax.bar_label(bars, labels=[f"{detection[rule][k]:.0f}%" for k in keys], padding=3)
ax.set(xticks=range(3), xticklabels=labels, ylabel="Rate (%)", ylim=(0, 119),
       title="Fixed-rule detection on 100 labeled synthetic images")
ax.legend(loc="upper right", frameon=False, fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(ROOT / "assets/detection.pdf", bbox_inches="tight")
fig.savefig(ROOT / "../evidence/final_detection/detection.png", dpi=170, bbox_inches="tight")
plt.close(fig)
print(f"Plots rebuilt from recorded results using Matplotlib {matplotlib.__version__}.")
