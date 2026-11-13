import os, re

def upgrade_biology_index():
    p = 'nsejs/biology/index.html'
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    new_tabs = """      <nav class="tabs" aria-label="NSEJS subject practice and Grade9 resources">
        <a href="../physics/index.html">⚛ Physics</a>
        <a href="../chemistry/index.html">🧪 Chemistry</a>
        <a href="index.html" aria-current="page">🧬 Biology</a>
        <a href="../index.html">🎯 NSEJS Hub</a>
        <a href="../../architecture/index.html">🧭 Architecture</a>
      </nav>"""
    html = re.sub(r'<nav class="tabs"[^>]*>.*?</nav>', new_tabs, html, flags=re.S)

    new_metrics = """    <!-- 4-Cell Metrics & Status Strip -->
    <section class="metrics-strip" aria-label="Biology curriculum metrics">
      <div class="metric-card">
        <span class="metric-num">5</span>
        <span class="metric-label">Biology Topics</span>
        <span class="metric-sub">Cell to Ecology</span>
      </div>
      <div class="metric-card">
        <span class="metric-num">119</span>
        <span class="metric-label">Candidate Questions</span>
        <span class="metric-sub">All Topics Indexed</span>
      </div>
      <div class="metric-card">
        <span class="metric-num">3</span>
        <span class="metric-label">Core 1A/1B Journeys</span>
        <span class="metric-sub">Authored &amp; Verified</span>
      </div>
      <div class="metric-card">
        <span class="metric-num">Rule 13</span>
        <span class="metric-label">Academic Status</span>
        <a href="../core2/question-map.html#biology" class="metric-sub" style="text-decoration:underline;">Browse 119 IDs Map →</a>
      </div>
    </section>"""
    html = re.sub(r'<!-- 4-Cell Metrics & Status Strip -->.*?<!-- Pill-Based Quick Filter Bar -->', new_metrics + '\n\n    <!-- Pill-Based Quick Filter Bar -->', html, flags=re.S)

    html = html.replace('<a class="primary-topic-btn" href="question-bank.html">', '<a class="primary-topic-btn" href="#topic-view">')

    new_bottom = """    <!-- Bottom 3-Card Supplementary Resources Deck -->
    <section class="bottom-resource-grid" aria-label="Supplementary learning and official source links">
      <div class="resource-box">
        <h3>Disciplinary Biology Curriculum</h3>
        <p>Explore all 5 biology domains structured hierarchically: Subject → Topic → Questions (Core 2) &amp; Core 1A/1B Lessons.</p>
        <a class="resource-btn btn-secondary" href="#topicsGrid">Browse All 5 Topics ↑</a>
      </div>
      <div class="resource-box">
        <h3>Core 2 Question Map</h3>
        <p>Comprehensive 267-item cross-subject question map with provenance verification, SHA-256 digests, and cognitive demand classifications.</p>
        <a class="resource-btn btn-secondary" href="../core2/question-map.html#biology">View Biology Question Map →</a>
      </div>
      <div class="resource-box">
        <h3>Official IAPT Exam Papers</h3>
        <p>10 official examination papers and publisher answer keys downloaded, SHA-256 verified, and archived in local custody.</p>
        <a class="resource-btn btn-secondary" href="../official-sources.html">View IAPT Source Downloads →</a>
      </div>
    </section>"""
    html = re.sub(r'<!-- Bottom 3-Card Supplementary Resources Deck -->.*?</section>', new_bottom, html, flags=re.S)

    topic_workspace = """    <!-- Interactive Disciplinary Topic Workspace: Core 1A/1B Lessons + Core 2 Questions -->
    <section id="topic-view" class="topic-workspace" style="margin: 40px 0 32px; padding: 28px 26px; border: 2px solid #86efac; border-radius: 18px; background: #ffffff; box-shadow: 0 4px 16px rgba(22,163,74,0.06); scroll-margin-top: 24px;">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
        <div>
          <span style="font-size:12px;font-weight:800;text-transform:uppercase;color:#16a34a;letter-spacing:0.07em;">Topic Deep-Dive &amp; Practice</span>
          <h2 style="font-size:22px;font-weight:800;margin:2px 0 0;color:#0f172a;">Topic Practice &amp; Core 1 Master Lessons</h2>
        </div>
        <span style="font-size:12px;font-weight:800;background:#dcfce7;color:#15803d;padding:5px 12px;border-radius:999px;border:1px solid #86efac;">
          Structure: Subject → Topic → Questions &amp; Lessons
        </span>
      </div>
      <nav id="topicNav" aria-label="Biology curriculum topics" style="display:flex;flex-wrap:wrap;gap:10px;margin:16px 0 20px 0;"></nav>
      <p id="status" role="status" style="font-size:14px;color:#64748b;margin:10px 0;">Loading candidate questions from biology-core2-candidates.v1.json…</p>
      <section id="questions" aria-label="Biology candidate questions"></section>
    </section>
"""
    if 'id="topic-view"' not in html:
        html = html.replace('<!-- Bottom 3-Card Supplementary Resources Deck -->', topic_workspace + '\n    <!-- Bottom 3-Card Supplementary Resources Deck -->')

    reader_script = """  <script>
    window.MathJax={tex:{inlineMath:[['$','$'],['\\\\(','\\\\)']]},svg:{fontCache:'global'}};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <script defer src="../js/core2-biology-reader.js"></script>"""
    if 'core2-biology-reader.js' not in html:
        html = html.replace('</body>', reader_script + '\n</body>')

    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Upgraded nsejs/biology/index.html")

def upgrade_chemistry_index():
    p = 'nsejs/chemistry/index.html'
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    new_tabs = """      <nav class="tabs" aria-label="NSEJS subject practice and Grade9 resources">
        <a href="../physics/index.html">⚛ Physics</a>
        <a href="index.html" aria-current="page">🧪 Chemistry</a>
        <a href="../biology/index.html">🧬 Biology</a>
        <a href="../index.html">🎯 NSEJS Hub</a>
        <a href="../../architecture/index.html">🧭 Architecture</a>
      </nav>"""
    html = re.sub(r'<nav class="tabs"[^>]*>.*?</nav>', new_tabs, html, flags=re.S)

    new_metrics = """    <!-- 4-Cell Metrics & Status Strip -->
    <section class="metrics-strip" aria-label="Chemistry curriculum metrics">
      <div class="metric-card">
        <span class="metric-num">6</span>
        <span class="metric-label">Chemistry Topics</span>
        <span class="metric-sub">Atom to Eudiometry</span>
      </div>
      <div class="metric-card">
        <span class="metric-num">119</span>
        <span class="metric-label">Candidate Questions</span>
        <span class="metric-sub">All Topics Indexed</span>
      </div>
      <div class="metric-card">
        <span class="metric-num">7</span>
        <span class="metric-label">Core 1A/1B Journeys</span>
        <span class="metric-sub">Authored &amp; Verified</span>
      </div>
      <div class="metric-card">
        <span class="metric-num">Rule 13</span>
        <span class="metric-label">Academic Status</span>
        <a href="../core2/question-map.html#chemistry" class="metric-sub" style="text-decoration:underline;">Browse 119 IDs Map →</a>
      </div>
    </section>"""
    html = re.sub(r'<!-- 4-Cell Metrics & Status Strip -->.*?<!-- Pill-Based Quick Filter Bar -->', new_metrics + '\n\n    <!-- Pill-Based Quick Filter Bar -->', html, flags=re.S)

    new_bottom = """    <!-- Bottom 3-Card Supplementary Resources Deck -->
    <section class="bottom-resource-grid" aria-label="Supplementary learning and official source links">
      <div class="resource-box">
        <h3>Disciplinary Chemistry Curriculum</h3>
        <p>Explore all 6 chemistry domains structured hierarchically: Subject → Topic → Questions (Core 2) &amp; Core 1A/1B Lessons.</p>
        <a class="resource-btn btn-secondary" href="#topicsGrid">Browse All 6 Topics ↑</a>
      </div>
      <div class="resource-box">
        <h3>Core 2 Question Map</h3>
        <p>Comprehensive 267-item cross-subject question map with provenance verification, SHA-256 digests, and cognitive demand classifications.</p>
        <a class="resource-btn btn-secondary" href="../core2/question-map.html#chemistry">View Chemistry Question Map →</a>
      </div>
      <div class="resource-box">
        <h3>Official IAPT Exam Papers</h3>
        <p>10 official examination papers and publisher answer keys downloaded, SHA-256 verified, and archived in local custody.</p>
        <a class="resource-btn btn-secondary" href="../official-sources.html">View IAPT Source Downloads →</a>
      </div>
    </section>"""
    html = re.sub(r'<!-- Bottom 3-Card Supplementary Resources Deck -->.*?</section>', new_bottom, html, flags=re.S)

    topic_workspace = """    <!-- Interactive Disciplinary Topic Workspace: Core 1A/1B Lessons + Core 2 Questions -->
    <section id="topic-view" class="topic-workspace" style="margin: 40px 0 32px; padding: 28px 26px; border: 2px solid #5eead4; border-radius: 18px; background: #ffffff; box-shadow: 0 4px 16px rgba(13,148,136,0.06); scroll-margin-top: 24px;">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
        <div>
          <span style="font-size:12px;font-weight:800;text-transform:uppercase;color:#0d9488;letter-spacing:0.07em;">Topic Deep-Dive &amp; Practice</span>
          <h2 style="font-size:22px;font-weight:800;margin:2px 0 0;color:#0f172a;">Topic Practice &amp; Core 1 Master Lessons</h2>
        </div>
        <span style="font-size:12px;font-weight:800;background:#ccfbf1;color:#0f766e;padding:5px 12px;border-radius:999px;border:1px solid #5eead4;">
          Structure: Subject → Topic → Questions &amp; Lessons
        </span>
      </div>
      <nav id="topicNav" aria-label="Chemistry curriculum topics" style="display:flex;flex-wrap:wrap;gap:10px;margin:16px 0 20px 0;"></nav>
      <p id="status" role="status" style="font-size:14px;color:#64748b;margin:10px 0;">Loading candidate questions from chemistry-core2-candidates.v1.json…</p>
      <section id="questions" aria-label="Chemistry candidate questions"></section>
    </section>
"""
    if 'id="topic-view"' not in html:
        html = html.replace('<!-- Bottom 3-Card Supplementary Resources Deck -->', topic_workspace + '\n    <!-- Bottom 3-Card Supplementary Resources Deck -->')

    reader_script = """  <script>
    window.MathJax={tex:{inlineMath:[['$','$'],['\\\\(','\\\\)']]},svg:{fontCache:'global'}};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <script defer src="../js/core2-chemistry-reader.js"></script>"""
    if 'core2-chemistry-reader.js' not in html:
        html = html.replace('</body>', reader_script + '\n</body>')

    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Upgraded nsejs/chemistry/index.html")

def upgrade_physics_index():
    p = 'nsejs/physics/index.html'
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    new_tabs = """      <nav class="tabs" aria-label="NSEJS subject practice and Grade9 resources">
        <a href="index.html" aria-current="page">⚛ Physics</a>
        <a href="../chemistry/index.html">🧪 Chemistry</a>
        <a href="../biology/index.html">🧬 Biology</a>
        <a href="../index.html">🎯 NSEJS Hub</a>
        <a href="../../architecture/index.html">🧭 Architecture</a>
      </nav>"""
    html = re.sub(r'<nav class="tabs"[^>]*>.*?</nav>', new_tabs, html, flags=re.S)

    new_metrics = """    <!-- 4-Cell Metrics & Status Strip -->
    <section class="metrics-strip" aria-label="Physics curriculum metrics">
      <div class="metric-card">
        <span class="metric-num">6</span>
        <span class="metric-label">Physics Topics</span>
        <span class="metric-sub">Optics to Fluids</span>
      </div>
      <div class="metric-card">
        <span class="metric-num">95</span>
        <span class="metric-label">Candidate Questions</span>
        <span class="metric-sub">Indexed in Core 2</span>
      </div>
      <div class="metric-card">
        <span class="metric-num">16</span>
        <span class="metric-label">Core 1A/1B Journeys</span>
        <span class="metric-sub">Authored &amp; Verified</span>
      </div>
      <div class="metric-card">
        <span class="metric-num">Rule 13</span>
        <span class="metric-label">Academic Status</span>
        <a href="../core2/question-map.html#physics" class="metric-sub" style="text-decoration:underline;">Browse 95 IDs Map →</a>
      </div>
    </section>"""
    html = re.sub(r'<!-- 4-Cell Metrics & Status Strip -->.*?<!-- Pill-Based Quick Filter Bar -->', new_metrics + '\n\n    <!-- Pill-Based Quick Filter Bar -->', html, flags=re.S)

    html = re.sub(r'href="question-bank\.html\?topic=([^"]+)"', r'href="#topic-view"', html)
    html = re.sub(r'onclick="openTopicQBank\(\'([^\']+)\'\)"', r'onclick="window.location.hash=\'#topic-view\';"', html)

    new_bottom = """    <!-- Bottom 3-Card Supplementary Resources Deck -->
    <section class="bottom-resource-grid" aria-label="Supplementary learning and official source links">
      <div class="resource-box">
        <h3>Disciplinary Physics Curriculum</h3>
        <p>Explore all 6 physics domains structured hierarchically: Subject → Topic → Questions (Core 2) &amp; Core 1A/1B Lessons.</p>
        <a class="resource-btn btn-secondary" href="#topicsGrid">Browse All 6 Topics ↑</a>
      </div>
      <div class="resource-box">
        <h3>Mechanics Six-Stage Learner</h3>
        <p>Interactive collision and momentum simulator with independent Task A/B transfer practice.</p>
        <a class="resource-btn btn-secondary" href="learn-mechanics.html?source_uid=g9:PHYSICS:G9-AUTH-MECH-001&source_revision=65eadfb0dfc06b4dc3c910ade26d5f5d005efea00be5d7c4f8128b3d45c29259">Open Mechanics Simulator →</a>
      </div>
      <div class="resource-box">
        <h3>Official IAPT Exam Papers</h3>
        <p>10 official examination papers and publisher answer keys downloaded, SHA-256 verified, and archived in local custody.</p>
        <a class="resource-btn btn-secondary" href="../official-sources.html">View IAPT Source Downloads →</a>
      </div>
    </section>"""
    html = re.sub(r'<!-- Bottom 3-Card Supplementary Resources Deck -->.*?</section>', new_bottom, html, flags=re.S)

    topic_workspace = """    <!-- Interactive Disciplinary Topic Workspace: Core 1A/1B Lessons + Core 2 Questions -->
    <section id="topic-view" class="topic-workspace" style="margin: 40px 0 32px; padding: 28px 26px; border: 2px solid #7dd3fc; border-radius: 18px; background: #ffffff; box-shadow: 0 4px 16px rgba(2,132,199,0.06); scroll-margin-top: 24px;">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
        <div>
          <span style="font-size:12px;font-weight:800;text-transform:uppercase;color:#0284c7;letter-spacing:0.07em;">Topic Deep-Dive &amp; Practice</span>
          <h2 style="font-size:22px;font-weight:800;margin:2px 0 0;color:#0f172a;">Topic Practice &amp; Core 1 Master Lessons</h2>
        </div>
        <span style="font-size:12px;font-weight:800;background:#e0f2fe;color:#0369a1;padding:5px 12px;border-radius:999px;border:1px solid #7dd3fc;">
          Structure: Subject → Topic → Questions &amp; Lessons
        </span>
      </div>
      <nav id="topicNav" aria-label="Physics curriculum topics" style="display:flex;flex-wrap:wrap;gap:10px;margin:16px 0 20px 0;"></nav>
      <p id="status" role="status" style="font-size:14px;color:#64748b;margin:10px 0;">Loading candidate questions from physics-core2-candidates.v1.json…</p>
      <section id="questions" aria-label="Physics candidate questions"></section>
    </section>
"""
    if 'id="topic-view"' not in html:
        html = html.replace('<!-- Bottom 3-Card Supplementary Resources Deck -->', topic_workspace + '\n    <!-- Bottom 3-Card Supplementary Resources Deck -->')

    reader_script = """  <script>
    window.MathJax={tex:{inlineMath:[['$','$'],['\\\\(','\\\\)']]},svg:{fontCache:'global'}};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <script defer src="../js/core2-physics-reader.js"></script>"""
    if 'core2-physics-reader.js' not in html:
        html = html.replace('</body>', reader_script + '\n</body>')

    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Upgraded nsejs/physics/index.html")

if __name__ == '__main__':
    upgrade_biology_index()
    upgrade_chemistry_index()
    upgrade_physics_index()
