import os
import re
from pathlib import Path

root = Path('.')
nsejs_dir = root / 'nsejs'
html_files = sorted(list(nsejs_dir.rglob('*.html')))

results = []
total_broken_links = 0

for file_path in html_files:
    rel_path = file_path.relative_to(root).as_posix()
    content = file_path.read_text(encoding='utf-8')
    
    # 1. Title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else 'NO_TITLE'
    
    # 2. Viewport
    has_viewport = bool(re.search(r'<meta[^>]+name=[\'"]viewport[\'"]', content, re.IGNORECASE))
    
    # 3. Masthead header
    has_masthead = '<header class="mast">' in content or '<header class="site-header' in content or '<nav class="tabs"' in content
    
    # 4. Breadcrumbs or back navigation
    has_breadcrumbs = bool(re.search(r'class=[\'"][^\'"]*(breadcrumb|back-link|hero-breadcrumbs|back-btn)[^\'"]*[\'"]', content, re.IGNORECASE) or 
                          '← Back' in content or 'Home /' in content or 'Home</a> /' in content or 'Home</a> / ' in content or
                          'Back to' in content)
    
    # 5. Rule 13 invariant
    has_rule13 = bool('{Unvalidated}' in content or '{Core 2: Reviewed}' in content or 'HOLD' in content or 'Rule 13' in content)
    
    # 6. Links integrity
    hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', content)
    broken_links = []
    internal_links_count = 0
    for href in hrefs:
        if href.startswith('#') or href.startswith('http') or href.startswith('mailto:') or href.startswith('javascript:'):
            continue
        internal_links_count += 1
        clean_href = href.split('#')[0].split('?')[0]
        if not clean_href:
            continue
        target_path = (file_path.parent / clean_href).resolve()
        if not target_path.exists():
            broken_links.append((href, str(target_path)))
            total_broken_links += 1

    # 7. 48px touch targets check
    has_touch_compliance = ('min-height: 48px' in content or 'min-height:48px' in content or 
                            'min-height: 52px' in content or 'min-height:52px' in content or
                            'min-height: 56px' in content or 'min-height:56px' in content or
                            'tablet-12-7.css' in content)

    results.append({
        'file': rel_path,
        'url': f"http://localhost:8000/{rel_path}",
        'title': title,
        'has_viewport': has_viewport,
        'has_masthead': has_masthead,
        'has_breadcrumbs': has_breadcrumbs,
        'has_rule13': has_rule13,
        'internal_links_count': internal_links_count,
        'broken_links': broken_links,
        'has_touch_compliance': has_touch_compliance
    })

print(f"=== NSEJS SITE-WIDE AUDIT: {len(results)} PAGES INSPECTED ===")
print(f"Total internal links checked: {sum(r['internal_links_count'] for r in results)}")
print(f"Total broken links: {total_broken_links}")
print("-" * 80)

failures = []
for r in results:
    status = "PASS"
    issues = []
    if not r['has_viewport']:
        issues.append("MISSING_VIEWPORT")
    if not r['has_masthead']:
        issues.append("MISSING_MASTHEAD")
    if not r['has_breadcrumbs']:
        issues.append("MISSING_BREADCRUMBS")
    if not r['has_rule13']:
        issues.append("MISSING_RULE13")
    if r['broken_links']:
        issues.append(f"BROKEN_LINKS({len(r['broken_links'])})")
    if not r['has_touch_compliance']:
        issues.append("MISSING_TOUCH_COMPLIANCE")
        
    if issues:
        status = "WARN/FAIL: " + ", ".join(issues)
        failures.append((r['file'], issues, r['broken_links']))
        
    print(f"[{'OK' if not issues else 'ISSUE'}] {r['file']} | {status}")

if failures:
    print("\n=== DETAILED ISSUES ===")
    for f, issues, broken in failures:
        print(f"\nFile: {f}")
        print(f"  Issues: {issues}")
        for b_href, b_target in broken:
            print(f"  Broken Link: {b_href} -> {b_target}")
else:
    print("\nALL 43 PAGES PASSED STATIC AUDIT CHECKS!")
