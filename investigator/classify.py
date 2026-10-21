import json
import re
from pathlib import Path
from read_failures import load_failures, group_by_test


def extract_locator(text):
    """Find which element the test was waiting for, e.g. getByTestId('login-button')."""
    match = re.search(r"waiting for ((?:getBy\w+|locator)\(.*?\))", text)
    return match.group(1) if match else None


def classify(title, attempts):
    first = attempts[0]
    text = first["errorMessage"]
    failed_every_time = len(attempts) > 1
    location = first.get("errorLocation")
    where = f"{Path(location['file']).name}:{location['line']}" if location else "unknown line"

    # Rule 1: environment problems (server or network down)
    env_patterns = ["ECONNREFUSED", "ERR_CONNECTION", "net::ERR", "ENOTFOUND", "502", "503", "504"]
    for pattern in env_patterns:
        if pattern in text:
            return {
                "classification": "environment",
                "confidence": 0.8,
                "likely_cause": "The test could not reach the server or network.",
                "evidence": [f"Error message contains '{pattern}'"],
                "debug_steps": [
                    "Check that the app/server was running during the test",
                    "Check CI network access and the base URL",
                ],
            }

    # Rule 2: failed once, then passed on retry -> flaky
    if not failed_every_time and first["retryNumber"] == 0:
        return {
            "classification": "flaky",
            "confidence": 0.6,
            "likely_cause": "The test failed once but passed on retry, so it is not consistently broken.",
            "evidence": ["Only 1 failed attempt; the retry passed"],
            "debug_steps": [
                "Look for timing problems: missing waits, animations, slow responses",
                "Run the test 20 times and check how often it fails",
            ],
        }

        # Rule 3: the element WAS found, but its text/value was wrong -> likely app bug
    if "Expected" in text and "Received" in text:
        expected = re.search(r"Expected:?\s*(.+)", text)
        received = re.search(r"Received:?\s*(.+)", text)
        expected = expected.group(1).strip() if expected else "?"
        received = received.group(1).strip() if received else "?"
        return {
            "classification": "app_bug",
            "confidence": 0.75 if failed_every_time else 0.5,
            "likely_cause": "The element was found, but the page showed different content than the test expected.",
            "evidence": [
                f"Expected {expected} but received {received}",
                "Playwright found the element, so the locator is fine" if "resolved to" in text else "Assertion mismatch in error",
                f"Failure happened at {where}",
            ],
            "debug_steps": [
                "Compare the expected and received values in the error",
                "Decide whether the app or the test expectation is wrong",
                "Check recent code changes to the feature",
            ],
        }

    # Rule 4: test cannot find an element -> locator problem
    locator = extract_locator(text)
    if locator:
        return {
            "classification": "locator",
            "confidence": 0.85 if failed_every_time else 0.6,
            "likely_cause": f"The test could not find the element {locator}. "
                            "The element may have been renamed or removed.",
            "evidence": [
                f"Error says it was waiting for {locator}",
                f"Failure happened at {where}",
                f"Failed on all {len(attempts)} attempts" if failed_every_time else "Failed once",
            ],
            "debug_steps": [
                f"Search the app code for {locator}: was it renamed or removed?",
                "Open the screenshot: is the element visible on the page?",
                "Update the locator in the test, or ask developers to restore it",
            ],
        }



if __name__ == "__main__":
    grouped = group_by_test(load_failures())
    results = {}

    for title, attempts in grouped.items():
        results[title] = classify(title, attempts)
        print(f"TEST: {title}")
        print(json.dumps(results[title], indent=2))
        print()

    out = Path(__file__).parent.parent / "failures" / "analysis.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Saved results to {out}")