import os

REDIRECTS = {
    'nsejs/biology/question-bank.html': {
        'target': 'index.html',
        'title': 'Biology Question Bank Consolidator · Grade9',
        'subject': 'Biology',
        'reason': 'Consolidated into unified Biology Topic Hub (Subject > Topic > Questions & Lessons)'
    },
    'nsejs/chemistry/question-bank.html': {
        'target': 'index.html',
        'title': 'Chemistry Question Bank Consolidator · Grade9',
        'subject': 'Chemistry',
        'reason': 'Consolidated into unified Chemistry Topic Hub (Subject > Topic > Questions & Lessons)'
    },
    'nsejs/physics/question-bank.html': {
        'target': 'index.html',
        'title': 'Physics Question Bank Consolidator · Grade9',
        'subject': 'Physics',
        'reason': 'Consolidated into unified Physics Topic Hub (Subject > Topic > Questions & Lessons)'
    },
    'nsejs/biology/authored-practice.html': {
        'target': 'index.html',
        'title': 'Biology Authored Practice Consolidator · Grade9',
        'subject': 'Biology',
        'reason': 'Consolidated into unified Biology Topic Hub'
    },
    'nsejs/chemistry/authored-practice.html': {
        'target': 'index.html',
        'title': 'Chemistry Authored Practice Consolidator · Grade9',
        'subject': 'Chemistry',
        'reason': 'Consolidated into unified Chemistry Topic Hub'
    },
    'nsejs/biology/core1/index.html': {
        'target': '../index.html',
        'title': 'Biology Core 1 Lessons Consolidator · Grade9',
        'subject': 'Biology',
        'reason': 'Consolidated into unified Biology Topic Hub'
    },
    'nsejs/chemistry/core1/index.html': {
        'target': '../index.html',
        'title': 'Chemistry Core 1 Lessons Consolidator · Grade9',
        'subject': 'Chemistry',
        'reason': 'Consolidated into unified Chemistry Topic Hub'
    },
    'nsejs/physics/core1/index.html': {
        'target': '../index.html',
        'title': 'Physics Core 1 Lessons Consolidator · Grade9',
        'subject': 'Physics',
        'reason': 'Consolidated into unified Physics Topic Hub'
    }
}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="0; url={target}">
  <title>{title}</title>
  <link rel="stylesheet" href="{rel_root}site.css">
  <link rel="stylesheet" href="{rel_root}css/tablet-12-7.css">
  <script>
    (function() {{
      const params = window.location.search || "";
      const hash = window.location.hash || "#topic-view";
      window.location.replace("{target}" + params + hash);
    }})();
  </script>
</head>
<body style="background:#f0f4f8;font-family:system-ui,sans-serif;margin:0;">
  <header class="mast">
    <div class="container top">
      <a class="logo" href="{rel_root}index.html"><i>G9</i>Grade9 v4.0</a>
      <nav class="tabs" aria-label="NSEJS subject practice and Grade9 resources">
        <a href="{rel_nsejs}physics/index.html"{phys_act}>⚛ Physics</a>
        <a href="{rel_nsejs}chemistry/index.html"{chem_act}>🧪 Chemistry</a>
        <a href="{rel_nsejs}biology/index.html"{bio_act}>🧬 Biology</a>
        <a href="{rel_nsejs}index.html">🎯 NSEJS Hub</a>
        <a href="{rel_root}architecture/index.html">🧭 Architecture</a>
      </nav>
    </div>
  </header>
  <main style="max-width:720px;margin:40px auto;background:white;padding:36px;border-radius:16px;border:1.5px solid #cbd5e1;box-shadow:0 10px 25px -5px rgba(0,0,0,0.06);text-align:center;">
    <nav class="breadcrumb-nav hero-breadcrumbs" style="margin-bottom:16px;font-size:13px;color:#64748b;">
      <a href="{rel_root}index.html">Home</a> / <a href="{rel_nsejs}index.html">NSEJS</a> / <a href="{target}">{subject} Hub</a> / <span>Consolidator Redirect</span>
    </nav>
    <span style="background:#e0f2fe;color:#0369a1;border:1px solid #0284c7;font-weight:800;font-size:12px;padding:4px 10px;border-radius:999px;">
      🛡️ {{Core 2: Reviewed}} · Curriculum Hierarchy Unified
    </span>
    <h1 style="font-size:24px;margin:16px 0 10px;color:#0f172a;">Redirecting to Unified {subject} Curriculum…</h1>
    <p style="color:#475569;font-size:15px;line-height:1.6;margin-bottom:24px;">
      {reason}. Standalone silo pages have been consolidated into the authentic academic hierarchy: <strong>Subject → Topic → Questions (Core 2) &amp; Core 1A/1B Lessons</strong>.
    </p>
    <a href="{target}" style="display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:12px 24px;background:#0284c7;color:white;font-weight:800;font-size:15px;border-radius:10px;text-decoration:none;">
      ← Back to {subject} Topic Hub
    </a>
  </main>
  <footer style="margin-top:30px;color:#64748b;font-size:13px;text-align:center;">
    Rule 13 Invariant: No academic approval inferred from software validation. Green CI means automatic tests passed; it never means student release is authorized.
  </footer>
</body>
</html>
"""

def generate_redirects():
    for rel_path, info in REDIRECTS.items():
        # calculate depth
        rel_from_nsejs = rel_path.replace('nsejs/', '')
        depth = rel_from_nsejs.count('/')
        rel_nsejs = '../' * depth if depth > 0 else ''
        rel_root = '../' * (depth + 1)
        
        subj = info['subject'].lower()
        phys_act = ' aria-current="page"' if subj == 'physics' else ''
        chem_act = ' aria-current="page"' if subj == 'chemistry' else ''
        bio_act = ' aria-current="page"' if subj == 'biology' else ''

        content = TEMPLATE.format(
            target=info['target'],
            title=info['title'],
            subject=info['subject'],
            reason=info['reason'],
            rel_root=rel_root,
            rel_nsejs=rel_nsejs,
            phys_act=phys_act,
            chem_act=chem_act,
            bio_act=bio_act
        )
        with open(rel_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated redirect: {rel_path} -> {info['target']}")

if __name__ == '__main__':
    generate_redirects()
