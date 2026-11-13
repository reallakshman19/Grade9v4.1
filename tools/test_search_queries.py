import json

with open("data/learner-search-index.v1.json", "r", encoding="utf-8") as f:
    docs = json.load(f)

test_cases = [
    ("NSEJS-2023-P-Q01", "all"),
    ("convex mirror", "nsejs"),
    ("eudiometry", "chemistry"),
    ("dihybrid", "biology"),
    ("work energy", "all"),
    ("titration", "nsejs"),
    ("surface tension", "nsejs"),
    ("resistor cube", "nsejs"),
    ("quantum bohr", "chemistry"),
    ("bacteriophage", "biology"),
]

print("=" * 80)
print(f"{'QUERY':20} {'SCOPE':12} {'MATCHES':8} {'TOP MATCH':38}")
print("=" * 80)
for q, s in test_cases:
    toks = q.lower().split()
    matched = [
        d for d in docs
        if (s == "all" or (s == "nsejs" and d.get("is_nsejs")) or d.get("subject", "").lower() == s)
        and all(t in d["search_text"] for t in toks)
    ]
    top_title = (matched[0]["title"][:34] + "…") if matched else "NONE"
    top_badge = matched[0]["badge"] if matched else ""
    print(f"{q:20} {s:12} {len(matched):<8} {top_title} [{top_badge}]")
print("=" * 80)
