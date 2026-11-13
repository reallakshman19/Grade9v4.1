import os
import re
from pathlib import Path

root = Path(".")
html_files = [f for f in root.glob("**/*.html") if ".git" not in str(f) and ".gemini" not in str(f)]

patterns = [
    ("question-bank.html", re.compile(r'href=["\'][^"\']*question-bank\.html[^"\']*["\']', re.I)),
    ("authored-practice.html", re.compile(r'href=["\'][^"\']*authored-practice\.html[^"\']*["\']', re.I)),
    ("core1/index.html", re.compile(r'href=["\'][^"\']*core1/index\.html[^"\']*["\']', re.I)),
    ("core1-recovery.html", re.compile(r'href=["\'][^"\']*core1-recovery\.html[^"\']*["\']', re.I)),
]

findings = []
for f in html_files:
    content = f.read_text(encoding="utf-8")
    is_redirect = 'http-equiv="refresh"' in content
    for name, pat in patterns:
        matches = pat.findall(content)
        if matches:
            findings.append((str(f), is_redirect, name, matches))

print(f"Total HTML files in repo: {len(html_files)}")
print(f"Total findings across repo: {len(findings)}")
for fpath, is_red, name, matches in findings:
    print(f"\nFile: {fpath} (is_redirect={is_red})")
    print(f"  Pattern: {name} ({len(matches)} matches)")
    for m in matches[:5]:
        print(f"    - {m}")
