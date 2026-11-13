import os, re, glob

html_files = glob.glob('nsejs/**/*.html', recursive=True)
print(f"Total HTML files found in nsejs: {len(html_files)}")

issues = []

for file in sorted(html_files):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check masthead
    has_mast = '<header class="mast">' in content or '<header class="top-nav">' in content
    
    # Check breadcrumb
    has_breadcrumb = 'breadcrumb' in content.lower() or 'breadcrumbs' in content.lower()
    
    # Check Agent A leaks
    has_agent_leak = bool(re.search(r'Agent\s+[AB]', content, re.I))
    
    # Check core1-recovery.html references
    has_recovery_ref = 'core1-recovery.html' in content
    
    rel_path = os.path.relpath(file, 'nsejs')
    
    status = []
    if not has_mast and 'core1-recovery.html' not in file:
        status.append("NO_MASTHEAD")
    if not has_breadcrumb and 'core1-recovery.html' not in file and file != 'nsejs/index.html':
        status.append("NO_BREADCRUMB")
    if has_agent_leak:
        status.append("AGENT_LEAK")
    if has_recovery_ref:
        status.append("CORE1_RECOVERY_REF")
        
    if status:
        issues.append((rel_path, status))

print(f"\nFiles with flags ({len(issues)}):")
for path, stat in issues:
    print(f"  {path}: {', '.join(stat)}")
