import json

with open('nsejs/data/chemistry-core2-candidates.v1.json', 'r', encoding='utf-8') as f:
    chem = json.load(f)

print(f"Total chem questions: {len(chem['questions'])}")
year_chem = [q for q in chem['questions'] if q['topic'].startswith('YEAR_')]
print(f"Year chem questions: {len(year_chem)}")
for q in year_chem[:10]:
    print(f"ID: {q['source_id']} | Topic: {q['topic']} | Stem: {q['stem'][:80]}...")

with open('nsejs/data/biology-core2-candidates.v1.json', 'r', encoding='utf-8') as f:
    bio = json.load(f)

print(f"\nTotal bio questions: {len(bio['questions'])}")
year_bio = [q for q in bio['questions'] if q['topic'].startswith('YEAR_')]
print(f"Year bio questions: {len(year_bio)}")
for q in year_bio[:10]:
    print(f"ID: {q['source_id']} | Topic: {q['topic']} | Stem: {q['stem'][:80]}...")
