import json
from pathlib import Path

# Find failures.json, no matter where we run the script from
FAILURES_FILE = Path(__file__).parent.parent / "failures" / "failures.json"


def load_failures():
    with open(FAILURES_FILE, encoding="utf-8") as f:
        return json.load(f)


def group_by_test(failures):
    """Group the attempts of the same test together (original run + retries)."""
    grouped = {}
    for failure in failures:
        title = failure["testTitle"]
        grouped.setdefault(title, []).append(failure)
    return grouped


if __name__ == "__main__":
    failures = load_failures()
    grouped = group_by_test(failures)

    print(f"Loaded {len(failures)} failed attempts from {len(grouped)} different tests.\n")

    for title, attempts in grouped.items():
        print(f"TEST: {title}")
        print(f"  Attempts that failed: {len(attempts)}")
        print(f"  Failed on every attempt: {len(attempts) > 1}")
        print(f"  Error: {attempts[0]['errorMessage'].strip()}")
        print()