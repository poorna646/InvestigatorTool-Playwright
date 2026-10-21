import json
import math
import re
from collections import Counter
from pathlib import Path
from read_failures import load_failures, group_by_test

KB_FILE = Path(__file__).parent.parent / "knowledge" / "past_bugs.json"


def tokenize(text):
    """Turn text into lowercase words: "getByTestId('login-button')" -> getbytestid, login, button"""
    return re.findall(r"[a-z0-9]+", text.lower())


def load_bugs():
    with open(KB_FILE, encoding="utf-8") as f:
        return json.load(f)


def bug_text(bug):
    return f"{bug['title']} {bug['error']} {bug['resolution']}"


def build_idf(documents):
    """Rare words get a high score, common words (in every bug) get a low score."""
    n = len(documents)
    doc_freq = Counter()
    for doc in documents:
        doc_freq.update(set(doc))
    return {w: math.log((n + 1) / (c + 1)) + 1 for w, c in doc_freq.items()}


def vectorize(tokens, idf):
    counts = Counter(tokens)
    return {w: c * idf[w] for w, c in counts.items() if w in idf}


def cosine(a, b):
    """How similar two word-score dictionaries are: 0 = nothing in common, 1 = identical."""
    dot = sum(v * b.get(w, 0) for w, v in a.items())
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def search(query, top_k=3):
    bugs = load_bugs()
    docs = [tokenize(bug_text(b)) for b in bugs]
    idf = build_idf(docs)
    query_vec = vectorize(tokenize(query), idf)

    scored = [(cosine(query_vec, vectorize(d, idf)), b) for d, b in zip(docs, bugs)]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [(score, bug) for score, bug in scored[:top_k] if score > 0]


if __name__ == "__main__":
    grouped = group_by_test(load_failures())
    title, attempts = next(iter(grouped.items()))
    query = attempts[0]["errorMessage"]

    print(f"Current failure: {title}")
    print(f"Searching memory with: {query.strip()}\n")

    for score, bug in search(query):
        print(f"{bug['id']}  similarity={score:.2f}  label={bug['label']}")
        print(f"  {bug['title']}")
        print(f"  Fix: {bug['resolution']}\n")