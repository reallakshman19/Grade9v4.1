import json

with open('nsejs/data/chemistry-core2-candidates.v1.json', 'r', encoding='utf-8') as f:
    chem = json.load(f)

print("Chemistry candidates topic distribution:")
chem_topics = {}
for q in chem['questions']:
    t = q.get('topic')
    chem_topics[t] = chem_topics.get(t, 0) + 1
for t, c in sorted(chem_topics.items()):
    print(f"  {t}: {c}")

with open('nsejs/data/biology-core2-candidates.v1.json', 'r', encoding='utf-8') as f:
    bio = json.load(f)

print("\nBiology candidates topic distribution:")
bio_topics = {}
for q in bio['questions']:
    t = q.get('topic')
    bio_topics[t] = bio_topics.get(t, 0) + 1
for t, c in sorted(bio_topics.items()):
    print(f"  {t}: {c}")
