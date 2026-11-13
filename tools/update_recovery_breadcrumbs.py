import glob, re

chem_files = glob.glob('nsejs/chemistry/core1/recovery/*/index.html')
phys_files = glob.glob('nsejs/physics/core1/recovery/*/index.html')

pattern = re.compile(
    r'<a href="\.\./\.\./\.\./\.\./core1-recovery\.html"[^>]*>[\s\S]*?18 Recovery Cases[\s\S]*?</a>',
    re.MULTILINE
)

print(f"Updating {len(chem_files)} chemistry files...")
for f in chem_files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    replacement = (
        '<a href="../../../question-bank.html" style="display:inline-flex;align-items:center;gap:6px;min-height:48px;'
        'padding:8px 16px;background:#f8fafc;color:#334155;border-radius:10px;text-decoration:none;font-weight:700;'
        'font-size:13.5px;border:1.5px solid #cbd5e1;">\n'
        '      📚 Chem Q-Bank\n'
        '    </a>'
    )
    new_c, count = pattern.subn(replacement, c)
    if count == 1:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(new_c)
        print(f"  ✓ {f}")
    else:
        print(f"  ✗ Pattern matched {count} times in {f}")

print(f"\nUpdating {len(phys_files)} physics files...")
for f in phys_files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    replacement = (
        '<a href="../../../question-bank.html" style="display:inline-flex;align-items:center;gap:6px;min-height:48px;'
        'padding:8px 16px;background:#f8fafc;color:#334155;border-radius:10px;text-decoration:none;font-weight:700;'
        'font-size:13.5px;border:1.5px solid #cbd5e1;">\n'
        '      📚 Physics Q-Bank\n'
        '    </a>'
    )
    new_c, count = pattern.subn(replacement, c)
    if count == 1:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(new_c)
        print(f"  ✓ {f}")
    else:
        print(f"  ✗ Pattern matched {count} times in {f}")

print("\nDone.")
