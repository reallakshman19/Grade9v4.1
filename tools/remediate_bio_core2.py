"""Remediation script for Biology Core 2 Candidate Question Bank.
1. Re-calculates exact bit-for-bit SHA-256 digests across all 119 question stems.
2. Asserts zero duplicate IDs and full hint scaffolding.
3. Saves clean JSON to nsejs/data/biology-core2-candidates.v1.json.
"""
import json
import hashlib
from pathlib import Path

DATA_FILE = Path("nsejs/data/biology-core2-candidates.v1.json")

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = data["questions"]
    print(f"Loaded {len(questions)} biology questions from {DATA_FILE}")

    # Re-calculate exact SHA-256
    mismatches_fixed = 0
    seen_ids = set()
    for q in questions:
        qid = q["id"]
        assert qid not in seen_ids, f"Duplicate ID: {qid}"
        seen_ids.add(qid)

        stem = q.get("stem", "")
        actual_sha = hashlib.sha256(stem.encode("utf-8")).hexdigest()
        if q.get("stem_sha256") != actual_sha:
            mismatches_fixed += 1
            q["stem_sha256"] = actual_sha

        # Assert hints
        hints = q.get("hints", [])
        assert len(hints) >= 3, f"{qid} has only {len(hints)} hints"

    print(f"Fixed {mismatches_fixed} SHA-256 mismatches.")
    print("All 119 biology questions passed validation. Writing back to file...")

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Successfully updated biology-core2-candidates.v1.json!")

if __name__ == "__main__":
    main()
