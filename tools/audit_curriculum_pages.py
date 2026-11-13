import os, re

pages = []
for root, dirs, files in os.walk('nsejs'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.relpath(os.path.join(root, f), 'nsejs')
            pages.append(p)

pages.sort()
print(f'Auditing {len(pages)} pages in nsejs/:\n')

for p in pages:
    full_p = os.path.join('nsejs', p)
    with open(full_p, 'r', encoding='utf-8', errors='ignore') as fp:
        html = fp.read()
    
    title_m = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
    title = title_m.group(1).strip() if title_m else 'NO TITLE'
    
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
    h1 = re.sub(r'<[^>]+>', '', h1_m.group(1)).strip() if h1_m else 'NO H1'
    
    # check links
    qb_links = re.findall(r'href=[\'"]([^\'"]*question-bank\.html[^\'"]*)[\'"]', html)
    ap_links = re.findall(r'href=[\'"]([^\'"]*authored-practice\.html[^\'"]*)[\'"]', html)
    rec_links = re.findall(r'href=[\'"]([^\'"]*core1-recovery\.html[^\'"]*)[\'"]', html)
    core1_idx = re.findall(r'href=[\'"]([^\'"]*core1/index\.html[^\'"]*)[\'"]', html)
    
    # check masthead tabs
    tabs_m = re.search(r'<nav class="tabs"[^>]*>(.*?)</nav>', html, re.I | re.S)
    tabs_text = re.sub(r'<[^>]+>', ' | ', tabs_m.group(1)).strip() if tabs_m else 'NO TABS'
    tabs_clean = ' '.join(tabs_text.split())
    
    flags = []
    if qb_links: flags.append(f'QB_LINKS({len(qb_links)})')
    if ap_links: flags.append(f'AUTH_PRAC_LINKS({len(ap_links)})')
    if rec_links: flags.append(f'REC_LINKS({len(rec_links)})')
    if core1_idx: flags.append(f'CORE1_IDX_LINKS({len(core1_idx)})')
    
    print(f'[{p}]')
    print(f'   Title:    {title[:70]}')
    print(f'   H1:       {h1[:70]}')
    print(f'   Masthead: {tabs_clean[:80]}')
    if flags:
        print(f'   Flags:    {" ".join(flags)}')
    print()
