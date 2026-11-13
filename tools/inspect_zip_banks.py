import zipfile, json, os

zpath = 'C:/Users/reall/.gemini/antigravity/brain/421e849e-f738-4afe-b89f-be94512c7468/.user_uploaded/media_1794559069877_00a8f430.zip'

with zipfile.ZipFile(zpath, 'r') as z:
    names = z.namelist()
    banks = {}
    for n in names:
        if n.endswith('questions.json'):
            parts = n.split('/')
            bank_id = parts[-2]
            raw = z.read(n).decode('utf-8')
            banks[bank_id] = json.loads(raw)

print(f'Total question banks extracted: {len(banks)}')

# Let's inspect chemistry banks
chem_banks = [k for k in banks if 'chem' in k]
bio_banks = [k for k in banks if 'bio' in k]
phys_banks = [k for k in banks if 'phys' in k or 'optics' in k or 'circuits' in k or 'electro' in k or 'magnet' in k or 'fluids' in k or 'mech' in k]

print('Chem banks:', chem_banks)
print('Bio banks:', bio_banks)
print('Phys banks:', len(phys_banks))

for b in chem_banks:
    print(f'  {b}: {len(banks[b])} questions')
    if len(banks[b]) > 0:
        sample = banks[b][0]
        print(f'    sample id: {sample.get("id")}, keys: {list(sample.keys())[:5]}')
