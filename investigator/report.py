from pathlib import Path

from read_failures import load_failures, group_by_test
from classify import classify
from memory import search

REPORT_FILE = Path(__file__).parent.parent / "failures" / "report.md"

# What kind of ticket each classification should become
TICKET_TYPE = {
    "app_bug": "Bug report (application)",
    "locator": "Test maintenance task (update the locator)",
    "flaky": "Flaky test ticket (stabilize the test)",
    "environment": "Infrastructure / environment issue",
    "unknown": "Needs manual investigation",
}


def find_attachment(attempt, name):
    for a in attempt["attachments"]:
        if a["name"] == name:
            return a["path"]
    return "not available"


def build_report(title, attempts):
    first = attempts[0]
    result = classify(title, attempts)
    similar = search(first["errorMessage"])

    lines = []
    lines.append(f"## {title}")
    lines.append("")
    lines.append(f"**Suggested ticket type:** {TICKET_TYPE[result['classification']]}")
    lines.append(f"**Classification:** {result['classification']} (confidence {result['confidence']})")
    lines.append(f"**Attempts that failed:** {len(attempts)}")
    lines.append(f"**Test file:** {Path(first['file']).name}, line {first['line']}")
    lines.append("")
    lines.append("### Likely cause")
    lines.append(result["likely_cause"])
    lines.append("")
    lines.append("### Evidence")
    for item in result["evidence"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("### Error message")
    lines.append("```")
    lines.append(first["errorMessage"].strip())
    lines.append("```")
    lines.append("")
    lines.append("### Suggested debugging steps")
    for i, step in enumerate(result["debug_steps"], 1):
        lines.append(f"{i}. {step}")
    lines.append("")
    lines.append("### Similar past bugs")
    if not similar:
        lines.append("No similar past bugs found.")
    for score, bug in similar:
        lines.append(f"- **{bug['id']}** ({bug['label']}, similarity {score:.2f}): {bug['title']}")
        lines.append(f"  - Past fix: {bug['resolution']}")
    if similar:
        agrees = similar[0][1]["label"] == result["classification"]
        note = "agrees with" if agrees else "does NOT agree with"
        lines.append("")
        lines.append(f"Memory check: the closest past bug {note} the classification.")
    lines.append("")
    lines.append("### Attachments")
    lines.append(f"- Screenshot: {find_attachment(first, 'screenshot')}")
    lines.append(f"- Trace: {find_attachment(first, 'trace')}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    grouped = group_by_test(load_failures())

    parts = ["# Failure investigation report", ""]
    for title, attempts in grouped.items():
        parts.append(build_report(title, attempts))
        parts.append("---")
        parts.append("")

    REPORT_FILE.write_text("\n".join(parts), encoding="utf-8")
    print(f"Investigated {len(grouped)} failing test(s).")
    print(f"Report saved to {REPORT_FILE}")