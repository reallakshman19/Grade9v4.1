import os, re

def check_pages():
    pages = []
    for root, dirs, files in os.walk('nsejs'):
        for f in files:
            if f.endswith('.html'):
                p = os.path.relpath(os.path.join(root, f), 'nsejs')
                pages.append(p)
    pages.sort()

    report = []
    for p in pages:
        full_p = os.path.join('nsejs', p)
        with open(full_p, 'r', encoding='utf-8', errors='ignore') as fp:
            html = fp.read()
        
        # Check navbar
        tabs_m = re.search(r'<nav class="tabs"[^>]*>(.*?)</nav>', html, re.I | re.S)
        tabs = tabs_m.group(1) if tabs_m else ''
        has_qb_in_nav = 'question-bank.html' in tabs or 'Q-Bank' in tabs
        has_core1_in_nav = 'core1/index.html' in tabs or 'Core 1 Lessons' in tabs
        
        # Check breadcrumbs
        crumbs_m = re.search(r'class="[^"]*breadcrumb[^"]*"[^>]*>(.*?)</(?:div|nav|p)>', html, re.I | re.S)
        crumbs = crumbs_m.group(1) if crumbs_m else ''
        has_core1_crumbs = 'Core 1 Lessons' in crumbs or 'core1-recovery' in crumbs
        
        # Check back buttons
        back_btns = re.findall(r'<a[^>]+href=[\'"]([^\'"]+)[\'"][^>]*>([^<]*Back[^<]*)</a>', html, re.I)
        
        # Check links to authored-practice
        has_auth_prac = 'authored-practice.html' in html
        has_rec_page = 'core1-recovery.html' in html
        
        issues = []
        if has_qb_in_nav:
            issues.append("QB_IN_NAV")
        if has_core1_in_nav:
            issues.append("CORE1_IN_NAV")
        if has_core1_crumbs:
            issues.append("CORE1_CRUMBS")
        if has_auth_prac and 'authored-practice.html' not in p:
            issues.append("LINKS_TO_AUTH_PRAC")
        if has_rec_page and 'core1-recovery.html' not in p:
            issues.append("LINKS_TO_CORE1_REC")
        
        report.append({
            'page': p,
            'issues': issues,
            'back_btns': back_btns
        })

    print(f"Total pages audited: {len(report)}")
    issues_found = [r for r in report if r['issues']]
    print(f"Pages with silo/patchy issues: {len(issues_found)}")
    for r in issues_found:
        print(f"  {r['page']:<55} -> {', '.join(r['issues'])}")

if __name__ == '__main__':
    check_pages()
