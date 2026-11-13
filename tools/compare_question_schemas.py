import json, zipfile

with open('nsejs/data/physics-core2-candidates.v1.json', 'r', encoding='utf-8') as f:
    phys_data = json.load(f)
phys_sample = phys_data['questions'][0]

print('Physics question fields:', list(phys_sample.keys()))

zpath = 'C:/Users/reall/.gemini/antigravity/brain/421e849e-f738-4afe-b89f-be94512c7468/.user_uploaded/media_1794559069877_00a8f430.zip'
with zipfile.ZipFile(zpath, 'r') as z:
    chem_topic_sample = json.loads(z.read('01_OWNER_PCB_NATIVE/individual_banks/chem-atomic-structure-r1/questions.json').decode('utf-8'))[0]
    chem_year_sample = json.loads(z.read('01_OWNER_PCB_NATIVE/individual_banks/nsejs-2023-chemistry-r1/questions.json').decode('utf-8'))[0]

print('Chem topic question fields:', list(chem_topic_sample.keys()))
print('Chem year question fields:', list(chem_year_sample.keys()))
