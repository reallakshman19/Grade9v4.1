import urllib.request, ssl, os, hashlib, json

os.makedirs('workspace/sources/iapt', exist_ok=True)

files = [
    ('2024_Set_51.pdf', 'https://iapt.org.in/wp-content/uploads/NSEJS-2024_Set_51.pdf'),
    ('2024_Final_Answer_Key.pdf', 'https://iapt.org.in/wp-content/uploads/NSEJS_-_2024_Final_Answer_Key.pdf'),
    ('2023_Set_51.pdf', 'https://iapt.org.in/wp-content/uploads/NSEJS_2023_Set_51.pdf'),
    ('2023_Tentative_Answer_Key.pdf', 'https://iapt.org.in/wp-content/uploads/NSEJS_2023_TENTATIVE_ANSWER_KEY.pdf'),
    ('2022_Set_51.pdf', 'https://iapt.org.in/wp-content/uploads/nsejs_2022_23_part_i.pdf'),
    ('2022_Final_Answer_Key.pdf', 'https://iapt.org.in/wp-content/uploads/nsejs-2022-final-answer-key.pdf'),
    ('2021_IOQJS_Part_I.pdf', 'https://iapt.org.in/wp-content/uploads/ioqjs_2021_22_part_i.pdf'),
    ('2021_IOQJS_Part_I_Answer_Key.pdf', 'https://iapt.org.in/wp-content/uploads/ioqjs_2021_22_part_i_answer_key.pdf'),
    ('2020_IOQJS_Part_I.pdf', 'https://iapt.org.in/wp-content/uploads/IOQJS-PART-I-2020-21.pdf'),
    ('2020_IOQJS_Part_I_Answer_Key.pdf', 'https://iapt.org.in/wp-content/uploads/Final-Answer-key-IOQJS-2020-21Part-I.pdf')
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

manifest = {}
for fname, url in files:
    dest = os.path.join('workspace/sources/iapt', fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f'Already exists: {fname} ({os.path.getsize(dest)} bytes)')
        with open(dest, 'rb') as f:
            data = f.read()
    else:
        print(f'Downloading {fname} from {url}...')
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            data = r.read()
        with open(dest, 'wb') as f:
            f.write(data)
        print(f'Saved {fname} ({len(data)} bytes)')
    
    sha = hashlib.sha256(data).hexdigest()
    manifest[fname] = {'url': url, 'bytes': len(data), 'sha256': sha}

manifest_path = 'workspace/sources/iapt/source_manifest.json'
with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

print('=== DOWNLOAD COMPLETE ===')
for k, v in manifest.items():
    print(f"{k}: {v['bytes']} bytes | sha256: {v['sha256'][:16]}...")
