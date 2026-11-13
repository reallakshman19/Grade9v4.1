import re

def update_bio_reader():
    p = 'nsejs/js/core2-biology-reader.js'
    with open(p, 'r', encoding='utf-8') as f:
        code = f.read()

    # Update line setting btn.href
    code = re.sub(
        r'btn\.href\s*=\s*"question-bank\.html\?topic="\s*\+\s*encodeURIComponent\(slug\);',
        'btn.href = "index.html?topic=" + encodeURIComponent(slug) + "#topic-view";',
        code
    )

    with open(p, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated core2-biology-reader.js")

def update_chem_reader():
    p = 'nsejs/js/core2-chemistry-reader.js'
    with open(p, 'r', encoding='utf-8') as f:
        code = f.read()

    code = re.sub(
        r'btn\.href\s*=\s*"question-bank\.html\?topic="\s*\+\s*encodeURIComponent\(slug\);',
        'btn.href = "index.html?topic=" + encodeURIComponent(slug) + "#topic-view";',
        code
    )

    with open(p, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated core2-chemistry-reader.js")

def update_phys_reader():
    p = 'nsejs/js/core2-physics-reader.js'
    with open(p, 'r', encoding='utf-8') as f:
        code = f.read()

    code = re.sub(
        r'a\.href\s*=\s*"question-bank\.html\?topic="\s*\+\s*encodeURIComponent\(t\[0\]\);',
        'a.href = "index.html?topic=" + encodeURIComponent(t[0]) + "#topic-view";',
        code
    )

    with open(p, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated core2-physics-reader.js")

if __name__ == '__main__':
    update_bio_reader()
    update_chem_reader()
    update_phys_reader()
