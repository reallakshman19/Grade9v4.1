import os, re

def standardize_masthead(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Calculate depth relative to nsejs
    rel_from_nsejs = os.path.relpath(file_path, 'nsejs').replace('\\', '/')
    depth = rel_from_nsejs.count('/')
    
    rel_nsejs = '../' * depth if depth > 0 else ''
    rel_root = '../' * (depth + 1)

    # Active subject
    is_phys = '/physics/' in f'/{rel_from_nsejs}' or rel_from_nsejs.startswith('physics/')
    is_chem = '/chemistry/' in f'/{rel_from_nsejs}' or rel_from_nsejs.startswith('chemistry/')
    is_bio = '/biology/' in f'/{rel_from_nsejs}' or rel_from_nsejs.startswith('biology/')
    is_hub = rel_from_nsejs == 'index.html'

    phys_act = ' aria-current="page"' if is_phys else ''
    chem_act = ' aria-current="page"' if is_chem else ''
    bio_act = ' aria-current="page"' if is_bio else ''
    hub_act = ' aria-current="page"' if is_hub else ''

    new_tabs = f"""      <nav class="tabs" aria-label="NSEJS subject practice and Grade9 resources">
        <a href="{rel_nsejs}physics/index.html"{phys_act}>⚛ Physics</a>
        <a href="{rel_nsejs}chemistry/index.html"{chem_act}>🧪 Chemistry</a>
        <a href="{rel_nsejs}biology/index.html"{bio_act}>🧬 Biology</a>
        <a href="{rel_nsejs}index.html"{hub_act}>🎯 NSEJS Hub</a>
        <a href="{rel_root}architecture/index.html">🧭 Architecture</a>
      </nav>"""

    # Check if nav.tabs exists
    if re.search(r'<nav class="tabs"[^>]*>.*?</nav>', html, flags=re.S):
        html = re.sub(r'<nav class="tabs"[^>]*>.*?</nav>', new_tabs, html, flags=re.S)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

def run():
    count = 0
    for root, dirs, files in os.walk('nsejs'):
        for f in files:
            if f.endswith('.html'):
                p = os.path.join(root, f)
                if standardize_masthead(p):
                    count += 1
    print(f"Standardized mastheads across {count} pages.")

if __name__ == '__main__':
    run()
