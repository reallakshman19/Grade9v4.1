import json

chem_file = 'nsejs/data/chemistry-core2-candidates.v1.json'
bio_file = 'nsejs/data/biology-core2-candidates.v1.json'

with open(chem_file, 'r', encoding='utf-8') as f:
    chem = json.load(f)

with open(bio_file, 'r', encoding='utf-8') as f:
    bio = json.load(f)

print("CHEMISTRY QUESTIONS TO CLASSIFY:")
for i, q in enumerate(chem['questions']):
    if q['topic'].startswith('YEAR_'):
        print(f"[{i}] {q['source_id']} ({q['topic']}): {q['stem'][:100]}...")

print("\n" + "="*80 + "\n")

print("BIOLOGY QUESTIONS TO CLASSIFY:")
for i, q in enumerate(bio['questions']):
    if q['topic'].startswith('YEAR_'):
        print(f"[{i}] {q['source_id']} ({q['topic']}): {q['stem'][:100]}...")
