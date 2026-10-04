# /// script
# requires-python = ">=3.11"
# ///
"""Check the format of a review report written by agent-instruction-review.

Usage: uv run check-review.py <report.md>
Prints "OK" and exits 0 when every check passes.
Prints one "NG: ..." line per finding and exits 1 otherwise.
"""

import re
import sys
from pathlib import Path

CATEGORIES = {
    "Information Safety",
    "Drift Resistance",
    "Documentation Responsibility",
    "ADR Separation",
    "Canonical Source",
    "Instruction Clarity",
    "Context Efficiency",
    "Universalizability",
    "Engineering Soundness",
    "Operational Sustainability",
    "Baseline Organization",
    "Constitution Mapping",
    "Constitution Consistency",
    "Article Scope",
    "Scope Inheritance",
    "Conflict Resolution",
}
VERDICTS = {
    "Adopt",
    "Revise",
    "Local-only",
    "Externalize",
    "Reject",
    "Human Decision Required",
}
FINDING_FIELDS = ("Finding", "Location", "Category", "Principle", "Reason", "Verdict")
CANDIDATE_FIELDS = (
    "Statement",
    "Derived-from",
    "Effect",
    "Engineering Soundness",
    "Operational Sustainability",
    "Verdict",
)
ENTRY = re.compile(r"^###\s+([FC]-\d+)\s*$")
HEADING = re.compile(r"^#{1,3}\s")
FIELD = re.compile(r"^- ([A-Za-z][A-Za-z -]*?):\s*(.*)$")
BLOCK_LABEL = re.compile(r"^(Before|After):\s*$")
MAXIMS = re.compile(r"^## Maxims\s*$", re.MULTILINE)
FENCE = re.compile(r"^\s*(```|~~~)")


def parse(lines):
    entries = []
    current = None
    in_fence = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = ENTRY.match(line)
        if match:
            current = {"id": match.group(1), "fields": {}, "blocks": set()}
            entries.append(current)
            continue
        if HEADING.match(line):
            current = None
            continue
        if current is None:
            continue
        match = FIELD.match(line)
        if match:
            current["fields"][match.group(1)] = match.group(2).strip()
            continue
        match = BLOCK_LABEL.match(line)
        if match:
            current["blocks"].add(match.group(1))
    return entries, in_fence


def check_finding(entry):
    fields, blocks = entry["fields"], entry["blocks"]
    findings = [f"{name} がない、または空" for name in FINDING_FIELDS if not fields.get(name)]
    category, verdict = fields.get("Category"), fields.get("Verdict")
    if category and category not in CATEGORIES:
        findings.append(f"Category `{category}` は決められた値ではない")
    if verdict and verdict not in VERDICTS:
        findings.append(f"Verdict `{verdict}` は決められた値ではない")
    if category == "Information Safety":
        if "Before" in blocks:
            findings.append("Information Safety の指摘に Before がある")
    elif verdict == "Revise":
        findings.extend(f"Revise の指摘に {name} がない" for name in ("Before", "After") if name not in blocks)
    if verdict == "Externalize" and not fields.get("Destination"):
        findings.append("Externalize の指摘に Destination がない")
    return findings


def check_candidate(entry):
    fields = entry["fields"]
    findings = [f"{name} がない、または空" for name in CANDIDATE_FIELDS if not fields.get(name)]
    verdict = fields.get("Verdict")
    if fields.get("Effect", "").startswith("なし"):
        findings.append("候補の Effect が「なし」になっている")
    if verdict == "Adopt":
        if not fields.get("Approval"):
            findings.append("Adopt の候補に Approval がない")
    elif verdict and verdict not in ("Human Decision Required", "Reject"):
        findings.append(f"候補の Verdict `{verdict}` は Human Decision Required、Adopt、Reject のどれでもない")
    return findings


def check(text):
    entries, open_fence = parse(text.splitlines())
    findings = []
    if open_fence:
        findings.append("閉じていないコードブロックがある")
    if not MAXIMS.search(text):
        findings.append("`## Maxims` の節がない")
    seen = set()
    for entry in entries:
        if entry["id"] in seen:
            findings.append(f"{entry['id']}: ID が重複している")
        seen.add(entry["id"])
        checker = check_finding if entry["id"].startswith("F") else check_candidate
        findings.extend(f"{entry['id']}: {finding}" for finding in checker(entry))
    return findings


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        print("Usage: uv run check-review.py <report.md>")
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"NG: {path} が見つからない")
        return 1
    findings = check(path.read_text(encoding="utf-8"))
    if not findings:
        print("OK")
        return 0
    for finding in findings:
        print(f"NG: {finding}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
