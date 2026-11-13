import json, zipfile, os

zpath = 'C:/Users/reall/.gemini/antigravity/brain/421e849e-f738-4afe-b89f-be94512c7468/.user_uploaded/media_1794559069877_00a8f430.zip'

with zipfile.ZipFile(zpath, 'r') as z:
    names = z.namelist()
    
    # Chemistry topic banks
    chem_topic_banks = [
        'chem-atomic-structure-r1',
        'chem-atomic-bonding-r1',
        'chem-chemical-substances-r1',
        'chem-matter-mole-r1'
    ]
    
    # Chemistry year banks
    chem_year_banks = [
        'nsejs-2024-chemistry-r1',
        'nsejs-2023-chemistry-r1',
        'nsejs-2022-chemistry-r1',
        'nsejs-2021-chemistry-r1',
        'nsejs-2020-chemistry-r1'
    ]
    
    # Biology topic banks
    bio_topic_banks = [
        'bio-environment-resources-r1',
        'bio-genetics-coordination-r1',
        'bio-life-processes-r1',
        'bio-organisation-living-world-r1'
    ]
    
    # Biology year banks
    bio_year_banks = [
        'nsejs-2024-biology-r1',
        'nsejs-2023-biology-r1',
        'nsejs-2022-biology-r1',
        'nsejs-2021-biology-r1',
        'nsejs-2020-biology-r1'
    ]
    
    # Physics year banks
    phys_year_banks = [
        'nsejs-2024-physics-r1',
        'nsejs-2023-physics-r1',
        'nsejs-2022-physics-r1',
        'nsejs-2021-physics-r1',
        'nsejs-2020-physics-r1'
    ]

    print('=== CHEMSITRY INVENTORY ===')
    chem_count = 0
    for b in chem_topic_banks + chem_year_banks:
        fn = f'01_OWNER_PCB_NATIVE/individual_banks/{b}/questions.json'
        cnt = len(json.loads(z.read(fn).decode('utf-8')))
        chem_count += cnt
        print(f'  {b}: {cnt} items')
    print(f'Total Chemistry questions available: {chem_count}')

    print('=== BIOLOGY INVENTORY ===')
    bio_count = 0
    for b in bio_topic_banks + bio_year_banks:
        fn = f'01_OWNER_PCB_NATIVE/individual_banks/{b}/questions.json'
        cnt = len(json.loads(z.read(fn).decode('utf-8')))
        bio_count += cnt
        print(f'  {b}: {cnt} items')
    print(f'Total Biology questions available: {bio_count}')

    print('=== PHYSICS INVENTORY ===')
    phys_count = 0
    for b in phys_year_banks:
        fn = f'01_OWNER_PCB_NATIVE/individual_banks/{b}/questions.json'
        cnt = len(json.loads(z.read(fn).decode('utf-8')))
        phys_count += cnt
        print(f'  {b}: {cnt} items')
    print(f'Total Physics year questions available: {phys_count} (in addition to existing 52 topic questions)')
