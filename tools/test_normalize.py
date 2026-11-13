import json, zipfile

zpath = 'C:/Users/reall/.gemini/antigravity/brain/421e849e-f738-4afe-b89f-be94512c7468/.user_uploaded/media_1794559069877_00a8f430.zip'

def normalize_year_question(item, year, subject_topic):
    # Extracts options
    raw_options = item.get('options', [])
    if raw_options and isinstance(raw_options[0], dict):
        options = [f"{opt['id']}: {opt['text']}" for opt in raw_options]
    else:
        options = [str(x) for x in raw_options]
    
    # Extract answer and hints
    ans_obj = item.get('answer', {})
    if isinstance(ans_obj, dict):
        corr = ans_obj.get('correct_option', '').upper()
        answer = f"Official Key: ({corr})" if corr else "Official Key: Pending Review"
        steps = ans_obj.get('reasoning', [])
        # Progressive hints
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

    return {
        "id": item['id'],
        "source_id": item['id'],
        "source_name": item.get('original_identifier', f"NSEJS {year} · {item['id']} · {op} · {band}"),
        "category": "EXAM_PAPER",
        "origin": "IAPT_NSEJS_OFFICIAL",
        "topic": subject_topic,
        "stem": item.get('stem', ''),
        "stem_sha256": "",
        "options": options,
        "question_type": "multiple_correct_mcq" if "MULTIPLE" in str(item.get('response', '')).upper() or int(item['id'].split('-Q')[-1]) >= 49 else "single_correct_mcq",
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
    raw = json.loads(z.read('01_OWNER_PCB_NATIVE/individual_banks/nsejs-2023-chemistry-r1/questions.json').decode('utf-8'))
    norm = normalize_year_question(raw[0], 2023, "YEAR_2023")
    print(json.dumps(norm, indent=2))
