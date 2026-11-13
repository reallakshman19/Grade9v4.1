import json

manifest = json.load(open('workspace/sources/iapt/source_manifest.json', 'r', encoding='utf-8'))
data = json.load(open('nsejs/data/source-linked-practice.v1.json', 'r', encoding='utf-8'))

data['source_authority'] = 'IAPT_OFFICIAL_PAPERS_DOWNLOADED_AND_HASH_VERIFIED'
data['downloaded_sources_count'] = len(manifest)

for yr in data['years']:
    y = yr['year']
    if y == 2024:
        yr['paper_url'] = manifest['2024_Set_51.pdf']['url']
        yr['key_url'] = manifest['2024_Final_Answer_Key.pdf']['url']
        yr['paper_bytes'] = manifest['2024_Set_51.pdf']['bytes']
        yr['paper_sha256'] = manifest['2024_Set_51.pdf']['sha256']
        yr['key_bytes'] = manifest['2024_Final_Answer_Key.pdf']['bytes']
        yr['key_sha256'] = manifest['2024_Final_Answer_Key.pdf']['sha256']
        yr['paper_evidence_status'] = 'OFFICIAL_IAPT_PDF_DOWNLOADED_AND_BYTE_VERIFIED'
        yr['key_evidence_status'] = 'OFFICIAL_IAPT_FINAL_KEY_DOWNLOADED_AND_BYTE_VERIFIED'
        yr['attempt_eligibility'] = 'OFFICIAL_DOWNLOAD_LOCAL_PRACTICE_SUPPORTED'
    elif y == 2023:
        yr['paper_url'] = manifest['2023_Set_51.pdf']['url']
        yr['key_url'] = manifest['2023_Tentative_Answer_Key.pdf']['url']
        yr['paper_bytes'] = manifest['2023_Set_51.pdf']['bytes']
        yr['paper_sha256'] = manifest['2023_Set_51.pdf']['sha256']
        yr['key_bytes'] = manifest['2023_Tentative_Answer_Key.pdf']['bytes']
        yr['key_sha256'] = manifest['2023_Tentative_Answer_Key.pdf']['sha256']
        yr['paper_evidence_status'] = 'OFFICIAL_IAPT_PDF_DOWNLOADED_AND_BYTE_VERIFIED'
        yr['key_evidence_status'] = 'OFFICIAL_IAPT_KEY_DOWNLOADED_AND_BYTE_VERIFIED'
        yr['attempt_eligibility'] = 'OFFICIAL_DOWNLOAD_LOCAL_PRACTICE_SUPPORTED'
        yr['paper_code'] = 51
        yr['supported_question_range'] = [1, 60]
        yr['multi_answer_range'] = [49, 60]
    elif y == 2022:
        yr['paper_url'] = manifest['2022_Set_51.pdf']['url']
        yr['key_url'] = manifest['2022_Final_Answer_Key.pdf']['url']
        yr['paper_bytes'] = manifest['2022_Set_51.pdf']['bytes']
        yr['paper_sha256'] = manifest['2022_Set_51.pdf']['sha256']
        yr['key_bytes'] = manifest['2022_Final_Answer_Key.pdf']['bytes']
        yr['key_sha256'] = manifest['2022_Final_Answer_Key.pdf']['sha256']
        yr['paper_evidence_status'] = 'OFFICIAL_IAPT_PDF_DOWNLOADED_AND_BYTE_VERIFIED'
        yr['key_evidence_status'] = 'OFFICIAL_IAPT_KEY_DOWNLOADED_AND_BYTE_VERIFIED'
        yr['attempt_eligibility'] = 'OFFICIAL_DOWNLOAD_LOCAL_PRACTICE_SUPPORTED'
        yr['paper_code'] = 51
        yr['supported_question_range'] = [1, 60]
        yr['multi_answer_range'] = [49, 60]
    elif y == 2021:
        yr['paper_url'] = manifest['2021_IOQJS_Part_I.pdf']['url']
        yr['key_url'] = manifest['2021_IOQJS_Part_I_Answer_Key.pdf']['url']
        yr['paper_bytes'] = manifest['2021_IOQJS_Part_I.pdf']['bytes']
        yr['paper_sha256'] = manifest['2021_IOQJS_Part_I.pdf']['sha256']
        yr['key_bytes'] = manifest['2021_IOQJS_Part_I_Answer_Key.pdf']['bytes']
        yr['key_sha256'] = manifest['2021_IOQJS_Part_I_Answer_Key.pdf']['sha256']
        yr['paper_evidence_status'] = 'OFFICIAL_IAPT_PDF_DOWNLOADED_AND_BYTE_VERIFIED'
        yr['key_evidence_status'] = 'OFFICIAL_IAPT_KEY_DOWNLOADED_AND_BYTE_VERIFIED'
        yr['attempt_eligibility'] = 'OFFICIAL_DOWNLOAD_LOCAL_PRACTICE_SUPPORTED'
        yr['supported_question_range'] = [1, 33]
    elif y == 2020:
        yr['paper_url'] = manifest['2020_IOQJS_Part_I.pdf']['url']
        yr['key_url'] = manifest['2020_IOQJS_Part_I_Answer_Key.pdf']['url']
        yr['paper_bytes'] = manifest['2020_IOQJS_Part_I.pdf']['bytes']
        yr['paper_sha256'] = manifest['2020_IOQJS_Part_I.pdf']['sha256']
        yr['key_bytes'] = manifest['2020_IOQJS_Part_I_Answer_Key.pdf']['bytes']
        yr['key_sha256'] = manifest['2020_IOQJS_Part_I_Answer_Key.pdf']['sha256']
        yr['paper_evidence_status'] = 'OFFICIAL_IAPT_PDF_DOWNLOADED_AND_BYTE_VERIFIED'
        yr['key_evidence_status'] = 'OFFICIAL_IAPT_KEY_DOWNLOADED_AND_BYTE_VERIFIED'
        yr['attempt_eligibility'] = 'OFFICIAL_DOWNLOAD_LOCAL_PRACTICE_SUPPORTED'
        yr['supported_question_range'] = [1, 24]

with open('nsejs/data/source-linked-practice.v1.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Updated nsejs/data/source-linked-practice.v1.json with downloaded custody records.")
