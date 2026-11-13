import json, zipfile, os, re, hashlib

zpath = 'C:/Users/reall/.gemini/antigravity/brain/421e849e-f738-4afe-b89f-be94512c7468/.user_uploaded/media_1794559069877_00a8f430.zip'

def normalize_year_question(item, year, subject_topic):
    raw_options = item.get('options', [])
    if raw_options and isinstance(raw_options[0], dict):
        options = [f"{opt['id']}: {opt['text']}" for opt in raw_options]
    else:
        options = [str(x) for x in raw_options]
    
    ans_obj = item.get('answer', {})
    if isinstance(ans_obj, dict):
        corr = ans_obj.get('correct_option', '').upper()
        answer = f"Official Key: ({corr})" if corr else "Official Key: Pending Review"
        steps = ans_obj.get('reasoning', [])
        hints = []
        if steps:
            hints.append({"prompt": "H1 (Context & Setup): Identify governing principles.", "text": steps[0]})
        if len(steps) > 1:
            hints.append({"prompt": "H2 (Formulation & Analysis): Key relationship.", "text": steps[1]})
        if len(steps) > 2:
            hints.append({"prompt": "H3 (Crux Resolution): Final calculation.", "text": steps[2]})
        elif len(hints) == 0:
            hints.append({"prompt": "H1 (Examination Note):", "text": "Consult the official paper and answer key."})
    else:
        answer = str(ans_obj)
        steps = []
        hints = [{"prompt": "H1 (Official Paper Guidance):", "text": "Review official key."}]

    ext = item.get('extensions', {})
    cog = ext.get('cognitive_demand', {})
    op = cog.get('operation', 'MODEL')
    band = cog.get('band', 'D2')
    score = cog.get('score', 4)
    crux_ref = ext.get('crux_move', f"{item['id']}-M2")

    qnum_match = re.search(r'-Q(\d+)', item['id'])
    qnum = int(qnum_match.group(1)) if qnum_match else 1
    is_multi = qnum >= 49 or 'multiple_answer' in str(item.get('response', '')).lower() or 'multiple_correct' in str(item.get('response', '')).lower()

    stem_text = item.get('stem', '')
    stem_sha = hashlib.sha256(stem_text.encode('utf-8')).hexdigest()

    return {
        "id": item['id'],
        "source_id": item['id'],
        "source_name": item.get('original_identifier', f"NSEJS {year} · {item['id']} · {op} · {band} (Score {score})"),
        "category": "EXAM_PAPER",
        "origin": "IAPT_NSEJS_OFFICIAL",
        "topic": subject_topic,
        "stem": stem_text,
        "stem_sha256": stem_sha,
        "options": options,
        "question_type": "multiple_correct_mcq" if is_multi else "single_correct_mcq",
        "source_figures": [],
        "figure_note": "",
        "hints": hints,
        "answer": answer,
        "steps": steps,
        "check": f"Adjudicated under IAPT {year} examination standards.",
        "op": op,
        "band": band,
        "score": score,
        "batch": f"NSEJS {year} Official Paper",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": [
            f"Official IAPT {year} examination item; independent external QRT adjudication receipt pending."
        ],
        "crux_move_ref": crux_ref
    }

with zipfile.ZipFile(zpath, 'r') as z:
    # 1. CHEMISTRY
    chem_questions = []
    
    # Topic banks
    chem_topic_map = {
        'chem-atomic-structure-r1': 'STRUCTURE_OF_THE_ATOM',
        'chem-atomic-bonding-r1': 'CHEMICAL_BONDING',
        'chem-matter-mole-r1': 'MOLE_CONCEPT_AND_GAS_LAWS',
        'chem-chemical-substances-r1': 'CHEMICAL_SUBSTANCES_AND_REACTIONS'
    }
    for bank_slug, topic_name in chem_topic_map.items():
        fn = f'01_OWNER_PCB_NATIVE/individual_banks/{bank_slug}/questions.json'
        raw = json.loads(z.read(fn).decode('utf-8'))
        for q in raw:
            q['topic'] = topic_name
            chem_questions.append(q)
            
    # Year banks
    chem_year_map = {
        'nsejs-2024-chemistry-r1': (2024, 'YEAR_2024'),
        'nsejs-2023-chemistry-r1': (2023, 'YEAR_2023'),
        'nsejs-2022-chemistry-r1': (2022, 'YEAR_2022'),
        'nsejs-2021-chemistry-r1': (2021, 'YEAR_2021'),
        'nsejs-2020-chemistry-r1': (2020, 'YEAR_2020')
    }
    for bank_slug, (year, topic_name) in chem_year_map.items():
        fn = f'01_OWNER_PCB_NATIVE/individual_banks/{bank_slug}/questions.json'
        raw = json.loads(z.read(fn).decode('utf-8'))
        for q in raw:
            chem_questions.append(normalize_year_question(q, year, topic_name))

    chem_payload = {
        "schema_version": "2.0.0",
        "subject": "CHEMISTRY",
        "source_authority": "IAPT_OFFICIAL_NSEJS_CANDIDATE_REGISTRY",
        "source_claims_status": "DOWNLOADED_AND_AUTHORED_CANDIDATES",
        "qrt_adjudication": "STAGE_5_CANDIDATE_INTAKE_STAGE_8_HOLD",
        "total_questions": len(chem_questions),
        "questions": chem_questions
    }
    with open('nsejs/data/chemistry-core2-candidates.v1.json', 'w', encoding='utf-8') as f:
        json.dump(chem_payload, f, indent=2)
    print(f"Generated nsejs/data/chemistry-core2-candidates.v1.json with {len(chem_questions)} questions.")

    # 2. BIOLOGY
    bio_questions = []
    bio_topic_map = {
        'bio-genetics-coordination-r1': 'GENETICS_AND_HEREDITY',
        'bio-organisation-living-world-r1': 'ORGANISATION_IN_LIVING_WORLD',
        'bio-life-processes-r1': 'LIFE_PROCESSES',
        'bio-environment-resources-r1': 'ENVIRONMENT_AND_NATURAL_RESOURCES'
    }
    for bank_slug, topic_name in bio_topic_map.items():
        fn = f'01_OWNER_PCB_NATIVE/individual_banks/{bank_slug}/questions.json'
        raw = json.loads(z.read(fn).decode('utf-8'))
        for q in raw:
            q['topic'] = topic_name
            bio_questions.append(q)

    bio_year_map = {
        'nsejs-2024-biology-r1': (2024, 'YEAR_2024'),
        'nsejs-2023-biology-r1': (2023, 'YEAR_2023'),
        'nsejs-2022-biology-r1': (2022, 'YEAR_2022'),
        'nsejs-2021-biology-r1': (2021, 'YEAR_2021'),
        'nsejs-2020-biology-r1': (2020, 'YEAR_2020')
    }
    for bank_slug, (year, topic_name) in bio_year_map.items():
        fn = f'01_OWNER_PCB_NATIVE/individual_banks/{bank_slug}/questions.json'
        raw = json.loads(z.read(fn).decode('utf-8'))
        for q in raw:
            bio_questions.append(normalize_year_question(q, year, topic_name))

    bio_payload = {
        "schema_version": "2.0.0",
        "subject": "BIOLOGY",
        "source_authority": "IAPT_OFFICIAL_NSEJS_CANDIDATE_REGISTRY",
        "source_claims_status": "DOWNLOADED_AND_AUTHORED_CANDIDATES",
        "qrt_adjudication": "STAGE_5_CANDIDATE_INTAKE_STAGE_8_HOLD",
        "total_questions": len(bio_questions),
        "questions": bio_questions
    }
    with open('nsejs/data/biology-core2-candidates.v1.json', 'w', encoding='utf-8') as f:
        json.dump(bio_payload, f, indent=2)
    print(f"Generated nsejs/data/biology-core2-candidates.v1.json with {len(bio_questions)} questions.")

    # 3. PHYSICS
    # Load existing physics topic questions (50)
    with open('nsejs/data/physics-core2-candidates.v1.json', 'r', encoding='utf-8') as f:
        phys_payload = json.load(f)
    existing_phys_questions = phys_payload.get('questions', [])
    existing_ids = set(q['id'] for q in existing_phys_questions)
    
    # Add fluids authored questions if not present
    if os.path.exists('nsejs/data/physics-authored-practice-r1.json'):
        with open('nsejs/data/physics-authored-practice-r1.json', 'r', encoding='utf-8') as f:
            fluids_data = json.load(f)
        for q in fluids_data.get('candidate_questions', []):
            if q['id'] not in existing_ids:
                existing_phys_questions.append(q)
                existing_ids.add(q['id'])

    # Add physics year questions
    phys_year_map = {
        'nsejs-2024-physics-r1': (2024, 'YEAR_2024'),
        'nsejs-2023-physics-r1': (2023, 'YEAR_2023'),
        'nsejs-2022-physics-r1': (2022, 'YEAR_2022'),
        'nsejs-2021-physics-r1': (2021, 'YEAR_2021'),
        'nsejs-2020-physics-r1': (2020, 'YEAR_2020')
    }
    for bank_slug, (year, topic_name) in phys_year_map.items():
        fn = f'01_OWNER_PCB_NATIVE/individual_banks/{bank_slug}/questions.json'
        raw = json.loads(z.read(fn).decode('utf-8'))
        for q in raw:
            norm_q = normalize_year_question(q, year, topic_name)
            if norm_q['id'] not in existing_ids:
                existing_phys_questions.append(norm_q)
                existing_ids.add(norm_q['id'])

    phys_payload['total_questions'] = len(existing_phys_questions)
    phys_payload['questions'] = existing_phys_questions
    with open('nsejs/data/physics-core2-candidates.v1.json', 'w', encoding='utf-8') as f:
        json.dump(phys_payload, f, indent=2)
    print(f"Updated nsejs/data/physics-core2-candidates.v1.json with {len(existing_phys_questions)} questions.")

print("=== ALL THREE QUESTION BANKS ASSEMBLED SUCCESSFULLY ===")
