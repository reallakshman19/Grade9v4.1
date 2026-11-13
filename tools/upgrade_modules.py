import os, sys, re
sys.path.insert(0, os.path.abspath('.'))
from tools.module_topic_registry import MODULE_TOPIC_MAP

SUBJECT_TITLES = {
    'physics': 'Physics',
    'chemistry': 'Chemistry',
    'biology': 'Biology'
}

def update_module(rel_path, mod_name, info):
    full_path = os.path.join('nsejs', rel_path)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return

    with open(full_path, 'r', encoding='utf-8') as f:
        html = f.read()

    subj = info['subject']
    subj_title = SUBJECT_TITLES[subj]
    topic_slug = info['topic_slug']
    topic_name = info['topic_name']

    # Determine depth relative to nsejs
    # e.g. chemistry/core1/chem-electronic-structure-d3-r1/index.html -> depth 3
    # e.g. chemistry/core1/recovery/chem-atomic-structure-r1/index.html -> depth 4
    depth = rel_path.count('/')
    
    # Path to nsejs root
    rel_nsejs = '../' * depth
    # Path to subject index
    rel_subj = '../' * (depth - 1)
    # Path to site root
    rel_root = '../' * (depth + 1)

    # 1. Update Masthead tabs
    phys_act = ' aria-current="page"' if subj == 'physics' else ''
    chem_act = ' aria-current="page"' if subj == 'chemistry' else ''
    bio_act = ' aria-current="page"' if subj == 'biology' else ''
    
    new_tabs = f"""      <nav class="tabs" aria-label="NSEJS subject practice and Grade9 resources">
        <a href="{rel_nsejs}physics/index.html"{phys_act}>⚛ Physics</a>
        <a href="{rel_nsejs}chemistry/index.html"{chem_act}>🧪 Chemistry</a>
        <a href="{rel_nsejs}biology/index.html"{bio_act}>🧬 Biology</a>
        <a href="{rel_nsejs}index.html">🎯 NSEJS Hub</a>
        <a href="{rel_root}architecture/index.html">🧭 Architecture</a>
      </nav>"""
    html = re.sub(r'<nav class="tabs"[^>]*>.*?</nav>', new_tabs, html, flags=re.S)

    # 2. Update Breadcrumb Navigation & Action Buttons
    # Find breadcrumb nav
    crumb_pattern = r'<nav class="breadcrumb-nav"[^>]*>.*?</nav>'
    crumb_match = re.search(crumb_pattern, html, flags=re.S)
    if crumb_match:
        old_crumb = crumb_match.group(0)
        # Extract title from old crumb
        last_span = re.findall(r'<span[^>]*>([^<]+)</span>', old_crumb)
        mod_display_title = last_span[-1].strip() if last_span else mod_name

        new_crumb = f"""<nav class="breadcrumb-nav" aria-label="Breadcrumb navigation" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:20px;padding:10px 0;border-bottom:1px solid #d2deea;">
  <div style="display:flex;align-items:center;gap:8px;font-size:14px;color:#475569;flex-wrap:wrap;">
    <a href="{rel_root}index.html" style="color:#0284c7;text-decoration:none;font-weight:700;">Home</a>
    <span>/</span>
    <a href="{rel_nsejs}index.html" style="color:#0284c7;text-decoration:none;font-weight:700;">NSEJS</a>
    <span>/</span>
    <a href="{rel_subj}index.html" style="color:#0284c7;text-decoration:none;font-weight:700;">{subj_title}</a>
    <span>/</span>
    <a href="{rel_subj}index.html?topic={topic_slug}" style="color:#0284c7;text-decoration:none;font-weight:700;">{topic_name}</a>
    <span>/</span>
    <span style="color:#0f172a;font-weight:750;">{mod_display_title}</span>
  </div>
  <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
    <a href="{rel_subj}index.html?topic={topic_slug}" style="display:inline-flex;align-items:center;gap:6px;min-height:48px;padding:8px 16px;background:#e0f2fe;color:#0369a1;border-radius:10px;text-decoration:none;font-weight:800;font-size:13.5px;border:1.5px solid #bae6fd;">
      ← Back to {topic_name}
    </a>
    <a href="{rel_subj}index.html?topic={topic_slug}#topic-view" style="display:inline-flex;align-items:center;gap:6px;min-height:48px;padding:8px 16px;background:#f0fdf4;color:#166534;border-radius:10px;text-decoration:none;font-weight:700;font-size:13.5px;border:1.5px solid #86efac;">
      📝 Practice Topic Questions
    </a>
  </div>
</nav>"""
        html = html.replace(old_crumb, new_crumb)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated module: {rel_path}")

def run():
    # Find all module index.html files
    for root, dirs, files in os.walk('nsejs'):
        for f in files:
            if f == 'index.html':
                full = os.path.normpath(os.path.join(root, f))
                rel = os.path.relpath(full, 'nsejs').replace('\\', '/')
                # Check if it matches any in MODULE_TOPIC_MAP
                for mod_name, info in MODULE_TOPIC_MAP.items():
                    if f"/{mod_name}/" in f"/{rel}":
                        update_module(rel, mod_name, info)

if __name__ == '__main__':
    run()
