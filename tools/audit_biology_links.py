import re
from pathlib import Path

def audit_file(filepath):
    print(f"=== Auditing {filepath} ===")
    content = Path(filepath).read_text(encoding="utf-8")
    
    # Check all anchors
    pattern = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.DOTALL | re.IGNORECASE)
    for m in pattern.finditer(content):
        attrs = m.group(1)
        text = re.sub(r'<[^>]+>', ' ', m.group(2)).strip()
        text = re.sub(r'\s+', ' ', text)
        
        href_match = re.search(r'href=["\']([^"\']*)["\']', attrs)
        onclick_match = re.search(r'onclick=["\']([^"\']*)["\']', attrs)
        
        href = href_match.group(1) if href_match else ""
        onclick = onclick_match.group(1) if onclick_match else ""
        
        # Flag suspicious links
        is_suspicious = (
            href.startswith("#") or
            "javascript" in href or
            "topic-view" in href or
            not href or
            r"\'" in onclick or
            "#" in href
        )
        if is_suspicious:
            print(f"  [SUSPICIOUS LINK] text='{text}' | href='{href}' | onclick='{onclick}'")

if __name__ == "__main__":
    audit_file("nsejs/biology/index.html")
    audit_file("nsejs/biology/question-bank.html")
    audit_file("nsejs/biology/authored-practice.html")
