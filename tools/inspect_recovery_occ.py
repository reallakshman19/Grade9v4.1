import glob, os

files = glob.glob('nsejs/**/recovery/*/index.html', recursive=True)
print(f"Found {len(files)} recovery index.html files:")
for f in sorted(files):
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    count = c.count('core1-recovery.html')
    print(f"  {f}: {count} occurrences")
