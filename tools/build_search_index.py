#!/usr/bin/env python3
"""Build converged discovery search index for Grade9 v4.0.

Indexes:
1. Question Banks:
   - Physics Core 2 Candidates (50 items)
   - Chemistry Core 2 Candidates (119 items)
   - Biology Core 2 Candidates (119 items)
   - Authored Practice (Physics, Chemistry, Biology)
   - 2024 Code 51 Official Items
2. Interactive Master Lessons & Tablets (27 Core 1A/1B/2 modules + WPE Pilot)
3. Curriculum Topics & Subtopics
4. Portal Hubs & Verification Dossiers

Supports smart scoping:
- can filter strictly by "is_nsejs" / scope="nsejs"
- can filter by subject (Physics, Chemistry, Biology, Mathematics)
- can filter by category (question, tablet, curriculum, page)
- keyword synonyms expansion for robust query matching

Generates:
- data/learner-search-index.v1.json
- nsejs/data/learner-search-index.v1.json
- data/keyword-synonyms.v1.json
- data/learner-search-manifest.v1.json
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Comprehensive Domain Synonyms & Thesaurus
DEFAULT_SYNONYMS = [
    {
        "id": "SYN-PHY-OPTICS",
        "slug": "optics",
        "canonical_term": "ray optics",
        "aliases": [
            "optics", "ray optics", "geometric optics", "light", "mirror", "mirrors",
            "convex mirror", "concave mirror", "lens", "lenses", "convex lens", "concave lens",
            "focal length", "focal", "focus", "pole", "principal axis", "radius of curvature",
            "reflection", "refraction", "snell", "snell's law", "refractive index",
            "magnification", "real image", "virtual image", "image distance", "object distance",
            "prism", "dispersion", "angle of deviation", "minimum deviation",
            "displacement method", "conjugate foci", "screw lens", "biconvex", "plano-convex"
        ]
    },
    {
        "id": "SYN-PHY-FLUIDS",
        "slug": "fluids",
        "canonical_term": "fluid mechanics",
        "aliases": [
            "fluids", "fluid mechanics", "hydrostatics", "pressure", "atmospheric pressure",
            "density", "relative density", "buoyancy", "buoyant force", "upthrust",
            "archimedes", "archimedes principle", "flotation", "surface tension",
            "surface energy", "excess pressure", "capillarity", "meniscus", "viscosity",
            "terminal velocity", "poiseuille", "bernoulli", "equation of continuity",
            "sound", "sound waves", "speed of sound", "frequency", "wavelength", "resonance", "tuning fork"
        ]
    },
    {
        "id": "SYN-PHY-CIRCUITS",
        "slug": "circuits",
        "canonical_term": "current electricity and circuits",
        "aliases": [
            "circuit", "circuits", "current", "electric current", "voltage", "potential difference",
            "resistance", "resistor", "resistors", "ohm", "ohm's law", "equivalent resistance",
            "series", "parallel", "kirchhoff", "kcl", "kvl", "loop rule", "junction rule",
            "ladder", "infinite ladder", "resistor cube", "cube symmetry", "bridge", "wheatstone bridge",
            "power", "joule heating", "emf", "internal resistance", "battery", "cell", "capacitance", "capacitor"
        ]
    },
    {
        "id": "SYN-PHY-ELECTROSTATICS",
        "slug": "electrostatics",
        "canonical_term": "electrostatics",
        "aliases": [
            "electrostatics", "static electricity", "charge", "electric charge", "point charge",
            "coulomb", "coulomb's law", "electric field", "field lines", "electric flux", "gauss's law",
            "potential", "electrostatic potential", "deflection", "deflection in electric field",
            "charged particle", "trajectory", "equipotential", "dipole", "polarization"
        ]
    },
    {
        "id": "SYN-PHY-MAGNETISM",
        "slug": "magnetism",
        "canonical_term": "magnetic effects of current",
        "aliases": [
            "magnetism", "magnetic field", "magnetic flux", "lorentz force", "biot savart",
            "ampere's law", "solenoid", "toroid", "force on conductor", "fleming left hand rule",
            "right hand thumb rule", "electromagnetic induction", "faraday", "lenz's law",
            "induced emf", "terminal velocity in b-field", "conducting rail", "motional emf"
        ]
    },
    {
        "id": "SYN-PHY-MECHANICS",
        "slug": "mechanics",
        "canonical_term": "classical mechanics and dynamics",
        "aliases": [
            "mechanics", "kinematics", "dynamics", "motion", "straight line", "1d motion", "2d motion",
            "projectile", "trajectory", "velocity", "acceleration", "displacement", "speed",
            "newton", "newton's laws", "inertia", "force", "net force", "friction", "static friction",
            "kinetic friction", "coefficient of friction", "normal force", "tension", "pulley",
            "momentum", "conservation of momentum", "impulse", "collision", "elastic collision",
            "inelastic collision", "center of mass", "work", "power", "energy", "kinetic energy",
            "potential energy", "work energy theorem", "conservation of energy", "spring", "spring constant",
            "hooke's law", "vertical circle", "circular motion", "centripetal force", "gravity", "gravitation"
        ]
    },
    {
        "id": "SYN-CHEM-ATOM",
        "slug": "atomic-structure",
        "canonical_term": "structure of the atom",
        "aliases": [
            "atom", "atomic", "atomic structure", "structure of atom", "bohr", "bohr's model",
            "electron", "proton", "neutron", "nucleus", "energy level", "ground state",
            "excited state", "quantum", "quantum numbers", "principal quantum number",
            "orbital", "orbitals", "subshell", "s orbital", "p orbital", "d orbital",
            "aufbau", "hund's rule", "pauli exclusion", "electronic configuration",
            "photon", "wavelength", "rydberg", "spectral lines", "balmer", "lyman", "ionization energy"
        ]
    },
    {
        "id": "SYN-CHEM-BONDING",
        "slug": "chemical-bonding",
        "canonical_term": "chemical bonding and molecular structure",
        "aliases": [
            "bonding", "chemical bonding", "covalent bond", "ionic bond", "coordinate bond",
            "hydrogen bond", "lewis", "lewis dot structure", "octet rule", "vsepr", "vsepr theory",
            "molecular geometry", "shape", "linear", "trigonal", "tetrahedral", "bent",
            "hybridization", "sp", "sp2", "sp3", "dipole moment", "polar", "nonpolar",
            "electronegativity", "phosphorus oxyacids", "hypophosphorous", "orthophosphoric",
            "pyrophosphoric", "p-oh", "p=o", "p-h bond", "basicity", "reducing action"
        ]
    },
    {
        "id": "SYN-CHEM-MOLE",
        "slug": "mole-concept",
        "canonical_term": "mole concept and stoichiometry",
        "aliases": [
            "mole", "mole concept", "stoichiometry", "avogadro", "avogadro's number",
            "molar mass", "molecular mass", "formula unit mass", "percentage composition",
            "empirical formula", "molecular formula", "limiting reagent", "limiting reactant",
            "excess reagent", "theoretical yield", "percentage yield", "concentration",
            "molarity", "molality", "normality", "mole fraction", "ppm", "solution",
            "gas volume", "stp", "molar volume", "22.4", "eudiometry", "gas analysis",
            "hydrocarbon combustion", "explosion of gases", "gas contraction", "boyle", "charles"
        ]
    },
    {
        "id": "SYN-CHEM-REDOX",
        "slug": "redox",
        "canonical_term": "redox reactions",
        "aliases": [
            "redox", "redox reactions", "oxidation", "reduction", "oxidation number",
            "oxidation state", "oxidizing agent", "reducing agent", "electron transfer",
            "half reaction", "balancing redox", "ion electron method", "disproportionation",
            "comproportionation", "titration", "redox titration", "permanganate", "kmno4",
            "dichromate", "k2cr2o7", "iodometry", "iodimetry", "equivalence point", "end point", "indicator"
        ]
    },
    {
        "id": "SYN-BIO-GENETICS",
        "slug": "genetics",
        "canonical_term": "genetics and heredity",
        "aliases": [
            "genetics", "heredity", "inheritance", "mendel", "mendelian genetics", "gene", "genes",
            "allele", "alleles", "dominant", "recessive", "homozygous", "heterozygous",
            "genotype", "phenotype", "monohybrid", "dihybrid", "punnett square", "law of segregation",
            "independent assortment", "incomplete dominance", "codominance", "multiple alleles",
            "epistasis", "complementary genes", "chromosome", "chromosomes", "autosomes", "sex chromosomes",
            "karyotype", "dna", "rna", "mutation", "pedigree", "coordination", "hormone", "nervous system"
        ]
    },
    {
        "id": "SYN-BIO-IMMUNOLOGY",
        "slug": "immunology",
        "canonical_term": "immunology and host defense",
        "aliases": [
            "immunology", "immunity", "immune system", "defense", "host defense",
            "innate immunity", "adaptive immunity", "acquired immunity", "active immunity",
            "passive immunity", "antigen", "antigens", "antibody", "antibodies", "immunoglobulin",
            "iga", "igd", "ige", "igg", "igm", "b cell", "b lymphocytes", "t cell", "t lymphocytes",
            "helper t", "cytotoxic t", "macrophage", "phagocytosis", "inflammation",
            "vaccine", "vaccination", "immunization", "memory cells", "humoral immunity",
            "cell-mediated immunity", "allergy", "autoimmune", "pathogen", "bacteria"
        ]
    },
    {
        "id": "SYN-BIO-VIROLOGY",
        "slug": "virology",
        "canonical_term": "viral genetics and molecular biology",
        "aliases": [
            "virus", "viruses", "viral", "virology", "viral genetics", "bacteriophage", "phage",
            "capsid", "envelope", "genome", "dna virus", "rna virus", "retrovirus", "hiv",
            "reverse transcriptase", "lytic cycle", "lysogenic cycle", "prophage", "provirus",
            "viral replication", "transcription", "translation", "central dogma", "mrna", "trna"
        ]
    },
    {
        "id": "SYN-MATH-CORE",
        "slug": "mathematics",
        "canonical_term": "mathematics and geometry",
        "aliases": [
            "math", "mathematics", "algebra", "polynomial", "polynomials", "degree", "roots",
            "zeros", "coefficients", "vieta", "remainder theorem", "factor theorem",
            "quadratic", "cubic", "equation", "theory of equations", "system of equations",
            "coordinate geometry", "distance formula", "section formula", "slope", "line",
            "geometry", "euclid", "euclidean geometry", "axioms", "postulates",
            "vectors", "vector algebra", "magnitude", "unit vector", "dot product", "cross product"
        ]
    },
    {
        "id": "SYN-EXAM-NSEJS",
        "slug": "nsejs",
        "canonical_term": "national standard examination in junior science",
        "aliases": [
            "nsejs", "junior science", "iapt", "olympiad", "ijso", "stage 1",
            "exam", "paper", "code 51", "past paper", "pyq", "competition", "competitive"
        ]
    }
]


def normalize_text(text: str) -> str:
    """Normalize text into lowercased tokens separated by single spaces."""
    if not text:
        return ""
    # strip LaTeX markup brackets and backslashes for clean searching
    s = re.sub(r"\\[a-zA-Z]+", " ", str(text))
    s = re.sub(r"[\$\{\}\\\_\^~#%&]", " ", s)
    s = re.sub(r"[^a-zA-Z0-9\-\.\s]", " ", s)
    return " ".join(s.lower().split())


def get_synonyms_for_tokens(tokens: list[str], synonyms: list[dict]) -> list[str]:
    """Find related synonyms matching given tokens."""
    matches = set()
    for tok in tokens:
        if len(tok) < 3:
            continue
        for syn in synonyms:
            slug = syn.get("slug", "")
            canon = syn.get("canonical_term", "")
            aliases = syn.get("aliases", [])
            if tok in slug or tok in canon or any(tok in a for a in aliases):
                matches.update(aliases[:8])
    return list(matches)


def build_question_documents(repo_root: Path, synonyms: list[dict]) -> list[dict]:
    """Index all question items across Physics, Chemistry, Biology and Authored Practice."""
    docs = []
    seen_ids = set()

    sources = [
        ("physics", repo_root / "nsejs" / "data" / "physics-core2-candidates.v1.json", "Physics", "nsejs/physics/question-bank.html"),
        ("chemistry", repo_root / "nsejs" / "data" / "chemistry-core2-candidates.v1.json", "Chemistry", "nsejs/chemistry/question-bank.html"),
        ("biology", repo_root / "nsejs" / "data" / "biology-core2-candidates.v1.json", "Biology", "nsejs/biology/question-bank.html"),
    ]

    for subj_key, json_path, subj_name, qb_page in sources:
        if not json_path.exists():
            continue
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            questions = data.get("questions", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            for q in questions:
                qid = q.get("id") or q.get("source_id")
                if not qid or qid in seen_ids:
                    continue
                seen_ids.add(qid)

                stem = q.get("stem", "")
                title = stem[:120].strip() or f"{subj_name} Question {qid}"
                options = q.get("options", [])
                opts_text = " ".join(str(o) for o in options)
                hints = q.get("hints", [])
                hints_text = " ".join((h.get("text", "") if isinstance(h, dict) else str(h)) for h in hints)
                steps = q.get("steps", [])
                steps_text = " ".join(str(s) for s in steps)
                ans = q.get("answer", "")
                ans_text = str(ans)

                topic = q.get("topic", "").replace("_", " ").title()
                band = q.get("band", "D2")
                op = q.get("op", "MODEL")
                score = q.get("score", 4)
                batch = q.get("batch", "NSEJS Candidate")
                origin = q.get("origin", "IAPT_NSEJS_OFFICIAL")

                # Locator match (e.g. 2023 Code 51 Q43)
                loc_match = re.search(r"(\d{4})", batch) or re.search(r"-(\d{2,4})-", qid)
                year_str = loc_match.group(1) if loc_match else ""
                qnum_match = re.search(r"-Q(\d+)", qid) or re.search(r"-(\d+)$", qid)
                qnum_str = f"Q{int(qnum_match.group(1))}" if qnum_match else ""

                # Extract synonyms
                tokens = [normalize_text(topic), normalize_text(subj_name)]
                syns = get_synonyms_for_tokens(tokens, synonyms)

                badge = f"NSEJS · {band}"
                breadcrumb = f"NSEJS · {subj_name} · {topic} · {band} · {op}"

                search_vector = normalize_text(
                    f"{qid} {title} {stem} {opts_text} {hints_text} {steps_text} "
                    f"{subj_name} {topic} {band} {op} {batch} {origin} {year_str} {qnum_str} "
                    f"nsejs olympiad iapt junior science {' '.join(syns)}"
                )

                # Direct link with anchor and query param
                item_url = f"{qb_page}?q={qid}#{qid}"

                docs.append({
                    "id": f"Q-{qid}",
                    "original_id": qid,
                    "type": "QUESTION",
                    "category": "question",
                    "badge": badge,
                    "breadcrumb": breadcrumb,
                    "subject": subj_name,
                    "exam_family": "NSEJS",
                    "is_nsejs": True,
                    "scope": ["nsejs", subj_name.lower()],
                    "title": title,
                    "stem": stem,
                    "options": options,
                    "hints": hints,
                    "band": band,
                    "op": op,
                    "score": score,
                    "topic": topic,
                    "url": item_url,
                    "search_text": search_vector
                })
        except Exception as e:
            print(f"Error parsing question bank {json_path}: {e}")

    # Index Authored Practice
    auth_path = repo_root / "nsejs" / "data" / "physics-authored-practice-r1.json"
    if auth_path.exists():
        try:
            with open(auth_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for q in data.get("questions", []):
                qid = q.get("id")
                if not qid or qid in seen_ids:
                    continue
                seen_ids.add(qid)
                stem = q.get("stem", "")
                title = q.get("source_name", stem[:110])
                topic = q.get("topic", "Mechanics").replace("_", " ").title()
                badge = "{Reviewed} · PRACTICE"
                breadcrumb = f"NSEJS · Physics · {topic} · Authored Practice"
                search_vector = normalize_text(
                    f"{qid} {title} {stem} Physics {topic} mechanics practice authored nsejs"
                )
                docs.append({
                    "id": f"Q-{qid}",
                    "original_id": qid,
                    "type": "QUESTION",
                    "category": "question",
                    "badge": badge,
                    "breadcrumb": breadcrumb,
                    "subject": "Physics",
                    "exam_family": "NSEJS",
                    "is_nsejs": True,
                    "scope": ["nsejs", "physics"],
                    "title": title,
                    "stem": stem,
                    "options": q.get("options", []),
                    "hints": q.get("hints", []),
                    "band": q.get("band", "D2"),
                    "op": q.get("op", "TRANSFER"),
                    "score": 4,
                    "topic": topic,
                    "url": f"nsejs/physics/authored-practice.html?q={qid}#{qid}",
                    "search_text": search_vector
                })
        except Exception as e:
            print(f"Error indexing authored practice: {e}")

    return docs


def build_tablet_documents(repo_root: Path, synonyms: list[dict]) -> list[dict]:
    """Index all 27 Core 1 interactive lessons & recovery modules + WPE pilot."""
    docs = []

    # Map of all published interactive lessons
    tablets = [
        # Physics Core 1 Lessons
        {
            "id": "TAB-PHY-FLUIDS-SOUND",
            "title": "Fluids & Sound: Acoustic Waves and Hydrostatics",
            "subject": "Physics",
            "topic": "Fluids and Sound",
            "badge": "CORE 1A FOUNDATION",
            "url": "nsejs/physics/core1/nsejs-fluids-sound-r1/index.html",
            "is_nsejs": True,
            "desc": "Acoustic wave propagation, buoyancy, and hydrostatic pressure models."
        },
        {
            "id": "TAB-PHY-FLUIDS-SURFACE",
            "title": "Fluids & Surface Energy: Meniscus Dynamics & Interfacial Tension",
            "subject": "Physics",
            "topic": "Fluids and Surface Energy",
            "badge": "CORE 1A · D3",
            "url": "nsejs/physics/core1/nsejs-fluids-surface-energy-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Surface energy balance, capillary rise, and droplet excess pressure."
        },
        {
            "id": "TAB-PHY-OPTICS-DISP",
            "title": "Ray Optics: Bessel Displacement Method & Conjugate Foci",
            "subject": "Physics",
            "topic": "Ray Optics",
            "badge": "CORE 1A · D3",
            "url": "nsejs/physics/core1/nsejs-optics-displacement-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Bessel displacement formulation, focal length precision, and dual conjugate image analysis."
        },
        {
            "id": "TAB-PHY-OPTICS-CONJUGATE",
            "title": "IOQJS Optics: Conjugate Foci and Lens Precision Calibration",
            "subject": "Physics",
            "topic": "Ray Optics",
            "badge": "CORE 1A · D3",
            "url": "nsejs/physics/core1/recovery/ioqjs-optics-conjugate-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Conjugate points, lens formula calibration, and magnification relations."
        },
        {
            "id": "TAB-PHY-CIRCUITS-CUBE",
            "title": "Circuits: Resistor Cube 3D Symmetry & Mesh Analysis",
            "subject": "Physics",
            "topic": "Circuits",
            "badge": "CORE 1A · D3",
            "url": "nsejs/physics/core1/recovery/nsejs-circuits-cube-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Body diagonal, face diagonal, and edge equivalent resistance across 12 equal resistors."
        },
        {
            "id": "TAB-PHY-CIRCUITS-LADDER",
            "title": "Circuits: Infinite Resistance Ladder & Recurrence Relations",
            "subject": "Physics",
            "topic": "Circuits",
            "badge": "CORE 1A · D3",
            "url": "nsejs/physics/core1/recovery/nsejs-circuits-ladder-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Recurrence quadratic equations, infinite cascade reduction, and boundary termination."
        },
        {
            "id": "TAB-PHY-CIRCUITS-R1",
            "title": "Circuits: Kirchhoff Laws & Network Node Simplification",
            "subject": "Physics",
            "topic": "Circuits",
            "badge": "CORE 1A FOUNDATION",
            "url": "nsejs/physics/core1/recovery/nsejs-circuits-r1/index.html",
            "is_nsejs": True,
            "desc": "KCL junction current conservation, KVL loop potential drops, and bridge simplification."
        },
        {
            "id": "TAB-PHY-ELECTRO-DEFLECTION",
            "title": "Electrostatics: Charged Particle Deflection in Uniform Electric Field",
            "subject": "Physics",
            "topic": "Electrostatics",
            "badge": "CORE 1A · D3",
            "url": "nsejs/physics/core1/recovery/nsejs-electrostatics-deflection-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Parabolic trajectories, electrostatic acceleration, and exit deflection angles."
        },
        {
            "id": "TAB-PHY-ELECTRO-R1",
            "title": "Electrostatics: Coulomb Law, Point Charges & Field Superposition",
            "subject": "Physics",
            "topic": "Electrostatics",
            "badge": "CORE 1A FOUNDATION",
            "url": "nsejs/physics/core1/recovery/nsejs-electrostatics-r1/index.html",
            "is_nsejs": True,
            "desc": "Electric fields, Coulomb force vector addition, and electric potential energy."
        },
        {
            "id": "TAB-PHY-MAG-R1",
            "title": "Magnetism: Magnetic Force, Lorentz Law & Field Geometry",
            "subject": "Physics",
            "topic": "Magnetism",
            "badge": "CORE 1A FOUNDATION",
            "url": "nsejs/physics/core1/recovery/nsejs-magnetism-r1/index.html",
            "is_nsejs": True,
            "desc": "Biot-Savart field patterns, right-hand rule, and current-carrying wire interactions."
        },
        {
            "id": "TAB-PHY-MAG-TERMINAL",
            "title": "Magnetism: Conducting Rail Motion & Terminal Velocity in B-Field",
            "subject": "Physics",
            "topic": "Magnetism",
            "badge": "CORE 1A · D3",
            "url": "nsejs/physics/core1/recovery/nsejs-magnetism-terminal-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Motional EMF, electromagnetic braking, and asymptotic steady-state terminal velocity."
        },
        {
            "id": "TAB-PHY-MECH-R1",
            "title": "Mechanics: Newton Laws, Friction & Multi-Body Constraint Dynamics",
            "subject": "Physics",
            "topic": "Mechanics",
            "badge": "CORE 1A FOUNDATION",
            "url": "nsejs/physics/core1/recovery/nsejs-mechanics-r1/index.html",
            "is_nsejs": True,
            "desc": "Free body diagrams, normal contact force, static/kinetic friction, and acceleration."
        },
        {
            "id": "TAB-PHY-OPTICS-LENS-MIRROR",
            "title": "Ray Optics: Combined Lens-Mirror Optical System & Silvered Lens",
            "subject": "Physics",
            "topic": "Ray Optics",
            "badge": "CORE 1A · D3",
            "url": "nsejs/physics/core1/recovery/nsejs-optics-lens-mirror-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Refraction-reflection cascading, effective focal length of silvered biconvex lenses."
        },
        {
            "id": "TAB-PHY-OPTICS-PRISM",
            "title": "Ray Optics: Triangular Prism Dispersion & Angle of Minimum Deviation",
            "subject": "Physics",
            "topic": "Ray Optics",
            "badge": "CORE 1A · D3",
            "url": "nsejs/physics/core1/recovery/nsejs-optics-prism-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Refractive index formula, symmetric ray passage, and dispersion across wavelength."
        },
        {
            "id": "TAB-PHY-OPTICS-R1",
            "title": "Ray Optics: Reflection at Spherical Mirrors & Mirror Equation",
            "subject": "Physics",
            "topic": "Ray Optics",
            "badge": "CORE 1A FOUNDATION",
            "url": "nsejs/physics/core1/recovery/nsejs-optics-r1/index.html",
            "is_nsejs": True,
            "desc": "Convex and concave spherical mirrors, paraxial ray tracing, and focal length formula."
        },
        {
            "id": "TAB-PHY-OPTICS-SCREW",
            "title": "Ray Optics: Optical Bench Spherometer & Screw Gauge Lens Radii",
            "subject": "Physics",
            "topic": "Ray Optics",
            "badge": "CORE 1A · D3",
            "url": "nsejs/physics/core1/recovery/nsejs-optics-screw-lens-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Precision curvature measurement, spherometer pitch, and lens maker equation."
        },
        {
            "id": "TAB-PHY-LEARN-MECH",
            "title": "Physics Mechanics: Interactive 6-Stage Learning Route",
            "subject": "Physics",
            "topic": "Mechanics and WPE",
            "badge": "CORE 1B TRANSFER",
            "url": "nsejs/physics/learn-mechanics.html",
            "is_nsejs": True,
            "desc": "6-stage guided learner route: Predict, Attempt, Reconstruct, Diagnose, Repair, Boundary Test."
        },

        # Chemistry Core 1 Lessons
        {
            "id": "TAB-CHEM-ELECTRONIC",
            "title": "Chemistry: Electronic Structure, Orbitals & Quantum Transitions",
            "subject": "Chemistry",
            "topic": "Structure of the Atom",
            "badge": "CORE 1A · D3",
            "url": "nsejs/chemistry/core1/chem-electronic-structure-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Bohr hydrogen transitions, photon emission, Aufbau principle, and subshell occupancies."
        },
        {
            "id": "TAB-CHEM-PHOSPHORUS",
            "title": "Chemistry: Phosphorus Oxyacids, Basicity & Oxidation Numbers",
            "subject": "Chemistry",
            "topic": "Chemical Bonding",
            "badge": "CORE 1A · D3",
            "url": "nsejs/chemistry/core1/chem-phosphorus-oxyacids-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Structural formulas, P-OH ionizable protons, P-H reducing bonds, and oxidation states."
        },
        {
            "id": "TAB-CHEM-ATOM-R1",
            "title": "Chemistry: Atomic Structure, Subatomic Particles & Isotopes",
            "subject": "Chemistry",
            "topic": "Structure of the Atom",
            "badge": "CORE 1A FOUNDATION",
            "url": "nsejs/chemistry/core1/recovery/chem-atomic-structure-r1/index.html",
            "is_nsejs": True,
            "desc": "Rutherford gold foil, protons, neutrons, mass number, and nuclear stability."
        },
        {
            "id": "TAB-CHEM-SUBSTANCES-R1",
            "title": "Chemistry: Chemical Substances, Bonding Classes & Reactivity",
            "subject": "Chemistry",
            "topic": "Chemical Substances",
            "badge": "CORE 1A FOUNDATION",
            "url": "nsejs/chemistry/core1/recovery/chem-chemical-substances-r1/index.html",
            "is_nsejs": True,
            "desc": "Ionic vs covalent crystal lattices, displacement reactions, and solubility rules."
        },
        {
            "id": "TAB-CHEM-EUDIOMETRY",
            "title": "Chemistry: Eudiometry, Gas Explosion & Hydrocarbon Stoichiometry",
            "subject": "Chemistry",
            "topic": "Mole Concept & Gas Laws",
            "badge": "CORE 1A · D3",
            "url": "nsejs/chemistry/core1/recovery/chem-eudiometry-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Eudiometer tube gas volume contraction, oxygen consumption, and hydrocarbon empirical formula."
        },
        {
            "id": "TAB-CHEM-MOLE-R1",
            "title": "Chemistry: Matter & Mole Concept, Avogadro Constant & Gas Volumes",
            "subject": "Chemistry",
            "topic": "Mole Concept",
            "badge": "CORE 1A FOUNDATION",
            "url": "nsejs/chemistry/core1/recovery/chem-matter-mole-r1/index.html",
            "is_nsejs": True,
            "desc": "Molar mass conversions, stoichiometric coefficients, and limiting reagent determinations."
        },
        {
            "id": "TAB-CHEM-REDOX-TITRATION",
            "title": "Chemistry: Redox Titration, Permanganate Half-Reactions & Stoichiometry",
            "subject": "Chemistry",
            "topic": "Redox Reactions",
            "badge": "CORE 1A · D3",
            "url": "nsejs/chemistry/core1/recovery/chem-redox-titration-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "KMnO4 self-indicating titrations, oxalate reduction, electron transfer stoichiometry."
        },

        # Biology Core 1 Lessons
        {
            "id": "TAB-BIO-GENETICS",
            "title": "Biology: Genetics & Coordination, Alleles & Dihybrid Segregation",
            "subject": "Biology",
            "topic": "Genetics and Heredity",
            "badge": "CORE 1A FOUNDATION",
            "url": "nsejs/biology/core1/bio-genetics-coordination-r1/index.html",
            "is_nsejs": True,
            "desc": "Mendelian ratios, dominant/recessive epistasis, gamete combinations, and plant coordination."
        },
        {
            "id": "TAB-BIO-IMMUNOLOGY",
            "title": "Biology: Immunology & Host Defense, Antibodies & Adaptive Immunity",
            "subject": "Biology",
            "topic": "Immunology",
            "badge": "CORE 1A · D3",
            "url": "nsejs/biology/core1/bio-immunology-defense-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Antigen-antibody recognition, B-cell clonal selection, immunoglobulins, and vaccine memory."
        },
        {
            "id": "TAB-BIO-VIROLOGY",
            "title": "Biology: Viral Genetics, Bacteriophage Lytic Cycles & Molecular Replicators",
            "subject": "Biology",
            "topic": "Viral Genetics",
            "badge": "CORE 1A · D3",
            "url": "nsejs/biology/core1/bio-viral-genetics-d3-r1/index.html",
            "is_nsejs": True,
            "desc": "Retrovirus RNA-to-DNA reverse transcription, lysogenic genome insertion, and capsid self-assembly."
        },

        # Physics WPE Chapter & Interactive Pilot
        {
            "id": "TAB-PHY-WPE-PILOT",
            "title": "Physics WPE: Work, Power & Energy Interactive Master Lesson",
            "subject": "Physics",
            "topic": "Work, Power and Energy",
            "badge": "TECHNICAL PILOT",
            "url": "preview/physics-wpe.html",
            "is_nsejs": False,
            "desc": "Interactive simulation, energy bar charts, work-kinetic energy theorem, and conservative force fields."
        },
        {
            "id": "TAB-PHY-WPE-CHALLENGE",
            "title": "Physics WPE: Learn to Challenge 6-Stage Route",
            "subject": "Physics",
            "topic": "Work, Power and Energy",
            "badge": "CORE 1B TRANSFER",
            "url": "physics/wpe/learn-challenge.html",
            "is_nsejs": False,
            "desc": "Multi-stage cognitive ladder from foundational concept to rigorous analytical problem."
        }
    ]

    for tab in tablets:
        subj = tab["subject"]
        topic = tab["topic"]
        title = tab["title"]
        desc = tab["desc"]
        badge = tab["badge"]
        is_nsejs = tab["is_nsejs"]

        tokens = [normalize_text(subj), normalize_text(topic), normalize_text(title)]
        syns = get_synonyms_for_tokens(tokens, synonyms)

        search_vector = normalize_text(
            f"{tab['id']} {title} {desc} {subj} {topic} {badge} "
            f"core1 core1a core2 master lesson tablet interactive simulation "
            f"{'nsejs' if is_nsejs else 'physics wpe'} {' '.join(syns)}"
        )

        scope_list = [subj.lower()]
        if is_nsejs:
            scope_list.append("nsejs")

        docs.append({
            "id": tab["id"],
            "original_id": tab["id"],
            "type": "TABLET",
            "category": "tablet",
            "badge": badge,
            "breadcrumb": f"{'NSEJS · ' if is_nsejs else ''}{subj} · {topic} · {badge}",
            "subject": subj,
            "exam_family": "NSEJS" if is_nsejs else "GENERAL",
            "is_nsejs": is_nsejs,
            "scope": scope_list,
            "title": title,
            "url": tab["url"],
            "search_text": search_vector
        })

    return docs


def build_curriculum_and_page_documents(repo_root: Path, synonyms: list[dict]) -> list[dict]:
    """Index curriculum topics, portal hubs, question banks, and verification dossiers."""
    docs = []

    topics_and_pages = [
        # Major Hubs
        {
            "id": "PAGE-PORTAL-HOME",
            "title": "Grade9 v4.0 Portal: Choose Your Subject Hub",
            "type": "PAGE",
            "category": "page",
            "badge": "PORTAL HUB",
            "subject": "Common",
            "is_nsejs": False,
            "url": "index.html",
            "desc": "Main entry point for Physics, Mathematics, Chemistry, NSEJS Junior Science, and Architecture."
        },
        {
            "id": "PAGE-NSEJS-HUB",
            "title": "NSEJS Junior Science: Subject-wise Tracks & Question Banks",
            "type": "PAGE",
            "category": "page",
            "badge": "NSEJS MAIN",
            "subject": "Common",
            "is_nsejs": True,
            "url": "nsejs/index.html",
            "desc": "Complete Junior Science competition curriculum: Physics (17 modules), Chemistry (7 modules), Biology (3 modules), and Question Banks."
        },
        {
            "id": "PAGE-NSEJS-PHYSICS",
            "title": "NSEJS Physics Track: Optics, Fluids, Circuits, Mechanics",
            "type": "PAGE",
            "category": "page",
            "badge": "TRACK HUB",
            "subject": "Physics",
            "is_nsejs": True,
            "url": "nsejs/physics/index.html",
            "desc": "50 Core 2 candidate questions, 17 Core 1 interactive master lessons, and IAPT past-paper analysis."
        },
        {
            "id": "PAGE-NSEJS-CHEMISTRY",
            "title": "NSEJS Chemistry Track: Atomic Structure, Bonding, Mole, Redox",
            "type": "PAGE",
            "category": "page",
            "badge": "TRACK HUB",
            "subject": "Chemistry",
            "is_nsejs": True,
            "url": "nsejs/chemistry/index.html",
            "desc": "119 Core 2 candidate questions, 7 Core 1 interactive master lessons, eudiometry, and redox titration."
        },
        {
            "id": "PAGE-NSEJS-BIOLOGY",
            "title": "NSEJS Biology Track: Genetics, Immunology, Viral Genetics",
            "type": "PAGE",
            "category": "page",
            "badge": "TRACK HUB",
            "subject": "Biology",
            "is_nsejs": True,
            "url": "nsejs/biology/index.html",
            "desc": "119 Core 2 candidate questions, 3 Core 1 interactive master lessons, Mendelian inheritance, and defense."
        },
        {
            "id": "PAGE-QB-PHYSICS",
            "title": "NSEJS Physics Question Bank: 50 Core 2 Candidate Items",
            "type": "PAGE",
            "category": "page",
            "badge": "QUESTION BANK",
            "subject": "Physics",
            "is_nsejs": True,
            "url": "nsejs/physics/question-bank.html",
            "desc": "Searchable, filterable question bank with D1-D4 cognitive demand bands, QRT models, and hints."
        },
        {
            "id": "PAGE-QB-CHEMISTRY",
            "title": "NSEJS Chemistry Question Bank: 119 Core 2 Candidate Items",
            "type": "PAGE",
            "category": "page",
            "badge": "QUESTION BANK",
            "subject": "Chemistry",
            "is_nsejs": True,
            "url": "nsejs/chemistry/question-bank.html",
            "desc": "119 questions across Atomic Structure, Bonding, Mole Concept, and Redox with worked reasoning."
        },
        {
            "id": "PAGE-QB-BIOLOGY",
            "title": "NSEJS Biology Question Bank: 119 Core 2 Candidate Items",
            "type": "PAGE",
            "category": "page",
            "badge": "QUESTION BANK",
            "subject": "Biology",
            "is_nsejs": True,
            "url": "nsejs/biology/question-bank.html",
            "desc": "119 questions across Genetics, Coordination, Immunology, and Viral Biology with D1-D4 tags."
        },
        {
            "id": "PAGE-OFFICIAL-SOURCES",
            "title": "Official Examination Sources: 10/10 Verified IAPT Papers & Fingerprints",
            "type": "PAGE",
            "category": "page",
            "badge": "VERIFICATION",
            "subject": "Common",
            "is_nsejs": True,
            "url": "nsejs/official-sources.html",
            "desc": "Custody verification dossier with exact byte counts and SHA-256 fingerprints for official 2020-2024 IAPT papers."
        },
        {
            "id": "PAGE-CORE2-MAP",
            "title": "NSEJS Core 2 Master Inventory & Question Map",
            "type": "PAGE",
            "category": "page",
            "badge": "INVENTORY",
            "subject": "Common",
            "is_nsejs": True,
            "url": "nsejs/core2/index.html",
            "desc": "Master candidate question inventory across 45 module banks and 267 question candidates."
        },
        {
            "id": "PAGE-CORE1-RECOVERY",
            "title": "NSEJS Core 1 Recovery Hub: 27 Master Lessons Archive",
            "type": "PAGE",
            "category": "page",
            "badge": "RECOVERY",
            "subject": "Common",
            "is_nsejs": True,
            "url": "nsejs/core1-recovery.html",
            "desc": "Audited recovery catalogue of all 27 Core 1 lessons across Physics, Chemistry, and Biology."
        },
        {
            "id": "PAGE-PHY-WPE-QB",
            "title": "Physics WPE Question Bank: Work, Power & Energy",
            "type": "PAGE",
            "category": "page",
            "badge": "QUESTION BANK",
            "subject": "Physics",
            "is_nsejs": False,
            "url": "physics/wpe/question-bank.html",
            "desc": "WPE technical pilot question bank and cumulative review reader."
        },
        {
            "id": "PAGE-ARCH-GUIDEBOOK",
            "title": "Architecture Guidebook: Standards & Rule 13 Protocol",
            "type": "PAGE",
            "category": "page",
            "badge": "ARCHITECTURE",
            "subject": "Common",
            "is_nsejs": False,
            "url": "architecture/guidebook.html",
            "desc": "Technical standard operating procedure, cognitive demand calibration, and academic admission rules."
        },

        # Curriculum Topics
        {
            "id": "TOPIC-RAY-OPTICS",
            "title": "Curriculum: Ray Optics, Spherical Mirrors & Thin Lenses",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Physics",
            "is_nsejs": True,
            "url": "nsejs/physics/question-bank.html?topic=RAY_OPTICS",
            "desc": "Reflection, refraction, mirrors, lenses, prism dispersion, optical instruments, and displacement."
        },
        {
            "id": "TOPIC-FLUIDS",
            "title": "Curriculum: Fluid Mechanics, Hydrostatics & Surface Tension",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Physics",
            "is_nsejs": True,
            "url": "nsejs/physics/question-bank.html?topic=FLUIDS",
            "desc": "Pressure, Archimedes upthrust, surface energy, meniscus, viscosity, and acoustic sound waves."
        },
        {
            "id": "TOPIC-CIRCUITS",
            "title": "Curriculum: Current Electricity, Kirchhoff Laws & Resistor Networks",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Physics",
            "is_nsejs": True,
            "url": "nsejs/physics/question-bank.html?topic=CIRCUITS",
            "desc": "Ohm's law, series/parallel combinations, resistor cubes, infinite ladders, and bridge circuits."
        },
        {
            "id": "TOPIC-ELECTROSTATICS",
            "title": "Curriculum: Electrostatics, Coulomb Law & Electric Fields",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Physics",
            "is_nsejs": True,
            "url": "nsejs/physics/question-bank.html?topic=ELECTROSTATICS",
            "desc": "Coulomb's law, electrostatic potential, electric field lines, and charged particle deflection."
        },
        {
            "id": "TOPIC-MAGNETISM",
            "title": "Curriculum: Magnetism, Lorentz Force & Electromagnetic Induction",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Physics",
            "is_nsejs": True,
            "url": "nsejs/physics/question-bank.html?topic=MAGNETISM",
            "desc": "Magnetic fields, Biot-Savart, Fleming rules, motional EMF, and terminal velocity in magnetic fields."
        },
        {
            "id": "TOPIC-MECHANICS",
            "title": "Curriculum: Classical Mechanics, Newton Laws & Momentum",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Physics",
            "is_nsejs": True,
            "url": "nsejs/physics/question-bank.html?topic=MECHANICS",
            "desc": "Kinematics, Newton's laws of motion, friction, impulse, collisions, and work-energy theorem."
        },
        {
            "id": "TOPIC-CHEM-ATOM",
            "title": "Curriculum: Atomic Structure, Quantum Numbers & Electron Orbitals",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Chemistry",
            "is_nsejs": True,
            "url": "nsejs/chemistry/question-bank.html?topic=STRUCTURE_OF_THE_ATOM",
            "desc": "Bohr model, quantum numbers, subshell electronic configurations, Aufbau, and spectral photons."
        },
        {
            "id": "TOPIC-CHEM-BONDING",
            "title": "Curriculum: Chemical Bonding, Molecular Geometry & VSEPR Theory",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Chemistry",
            "is_nsejs": True,
            "url": "nsejs/chemistry/question-bank.html?topic=CHEMICAL_BONDING",
            "desc": "Covalent/ionic bonds, Lewis structures, VSEPR geometries, hybridization, and phosphorus oxyacids."
        },
        {
            "id": "TOPIC-CHEM-MOLE",
            "title": "Curriculum: Mole Concept, Stoichiometry, Gas Laws & Eudiometry",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Chemistry",
            "is_nsejs": True,
            "url": "nsejs/chemistry/question-bank.html?topic=MOLE_CONCEPT_AND_GAS_LAWS",
            "desc": "Avogadro constant, stoichiometric limiting reagents, gas volume contraction, and empirical formulas."
        },
        {
            "id": "TOPIC-CHEM-REDOX",
            "title": "Curriculum: Redox Reactions, Oxidation States & Titrations",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Chemistry",
            "is_nsejs": True,
            "url": "nsejs/chemistry/question-bank.html?topic=REDOX_REACTIONS",
            "desc": "Oxidation numbers, half-reactions, disproportionation, permanganate titrations, and electron transfer."
        },
        {
            "id": "TOPIC-BIO-GENETICS",
            "title": "Curriculum: Genetics, Heredity, Mendelian Laws & Chromosomes",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Biology",
            "is_nsejs": True,
            "url": "nsejs/biology/question-bank.html?topic=GENETICS_AND_HEREDITY",
            "desc": "Mendelian inheritance, dominant/recessive alleles, dihybrid ratios, epistasis, and chromosomes."
        },
        {
            "id": "TOPIC-BIO-IMMUNOLOGY",
            "title": "Curriculum: Immunology, Host Defense, Antibodies & Vaccines",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Biology",
            "is_nsejs": True,
            "url": "nsejs/biology/question-bank.html?topic=IMMUNOLOGY",
            "desc": "Innate vs adaptive immunity, antigen-antibody binding, clonal selection, and memory cells."
        },
        {
            "id": "TOPIC-BIO-VIROLOGY",
            "title": "Curriculum: Viral Genetics, Bacteriophage Cycles & Molecular Biology",
            "type": "TOPIC",
            "category": "curriculum",
            "badge": "CURRICULUM TOPIC",
            "subject": "Biology",
            "is_nsejs": True,
            "url": "nsejs/biology/question-bank.html?topic=VIRAL_GENETICS",
            "desc": "Retrovirus reverse transcription, lytic and lysogenic replication cycles, and nucleic acid genomes."
        }
    ]

    for item in topics_and_pages:
        subj = item["subject"]
        title = item["title"]
        desc = item["desc"]
        badge = item["badge"]
        is_nsejs = item["is_nsejs"]
        cat = item["category"]

        tokens = [normalize_text(subj), normalize_text(title), normalize_text(desc)]
        syns = get_synonyms_for_tokens(tokens, synonyms)

        search_vector = normalize_text(
            f"{item['id']} {title} {desc} {subj} {badge} {cat} "
            f"{'nsejs olympiad iapt junior science' if is_nsejs else 'portal'} {' '.join(syns)}"
        )

        scope_list = [subj.lower()]
        if is_nsejs:
            scope_list.append("nsejs")

        docs.append({
            "id": item["id"],
            "original_id": item["id"],
            "type": item["type"],
            "category": cat,
            "badge": badge,
            "breadcrumb": f"{'NSEJS · ' if is_nsejs else ''}{subj} · {badge}",
            "subject": subj,
            "exam_family": "NSEJS" if is_nsejs else "GENERAL",
            "is_nsejs": is_nsejs,
            "scope": scope_list,
            "title": title,
            "url": item["url"],
            "search_text": search_vector
        })

    return docs


def main():
    print("Building Grade9 v4.0 Search Index...")
    synonyms = DEFAULT_SYNONYMS

    q_docs = build_question_documents(REPO_ROOT, synonyms)
    tab_docs = build_tablet_documents(REPO_ROOT, synonyms)
    cur_docs = build_curriculum_and_page_documents(REPO_ROOT, synonyms)

    all_docs = q_docs + tab_docs + cur_docs

    # Stats
    stats = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_documents": len(all_docs),
        "by_category": {},
        "by_subject": {},
        "nsejs_count": sum(1 for d in all_docs if d.get("is_nsejs")),
        "non_nsejs_count": sum(1 for d in all_docs if not d.get("is_nsejs"))
    }

    for d in all_docs:
        c = d["category"]
        stats["by_category"][c] = stats["by_category"].get(c, 0) + 1
        s = d["subject"]
        stats["by_subject"][s] = stats["by_subject"].get(s, 0) + 1

    print(f"Total documents indexed: {len(all_docs)}")
    print(f"By category: {stats['by_category']}")
    print(f"By subject: {stats['by_subject']}")
    print(f"NSEJS documents: {stats['nsejs_count']} | General/Portal: {stats['non_nsejs_count']}")

    # Write output files
    out_dirs = [
        REPO_ROOT / "data",
        REPO_ROOT / "nsejs" / "data"
    ]
    for d in out_dirs:
        d.mkdir(parents=True, exist_ok=True)

    json_bytes = json.dumps(all_docs, indent=2, ensure_ascii=False).encode("utf-8")
    index_sha = hashlib.sha256(json_bytes).hexdigest()
    stats["sha256"] = index_sha

    # Write main data files
    for d in out_dirs:
        (d / "learner-search-index.v1.json").write_bytes(json_bytes)

    # Write synonyms and manifest
    (REPO_ROOT / "data" / "keyword-synonyms.v1.json").write_text(
        json.dumps({"$schema": "grade9v4-keyword-synonyms-v1", "synonyms": synonyms}, indent=2),
        encoding="utf-8"
    )
    (REPO_ROOT / "nsejs" / "data" / "keyword-synonyms.v1.json").write_text(
        json.dumps({"$schema": "grade9v4-keyword-synonyms-v1", "synonyms": synonyms}, indent=2),
        encoding="utf-8"
    )

    (REPO_ROOT / "data" / "learner-search-manifest.v1.json").write_text(
        json.dumps(stats, indent=2), encoding="utf-8"
    )
    (REPO_ROOT / "nsejs" / "data" / "learner-search-manifest.v1.json").write_text(
        json.dumps(stats, indent=2), encoding="utf-8"
    )

    print(f"Index built successfully! SHA256: {index_sha}")


if __name__ == "__main__":
    main()
