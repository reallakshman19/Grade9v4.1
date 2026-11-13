"""Remediation script for Chemistry Core 2 Candidate Question Bank.
Applies:
1. Disambiguation of duplicate IDs (indices 10..19 from ATOM-01..10 to BOND-01..10).
2. Authoring of complete 3-Tier Progressive Hint Scaffolds (H1, H2, H3) for ATOM-02..10.
3. Bit-for-bit re-calculation of exact SHA-256 digests across all 119 question stems.
4. Clean JSON formatting and preservation of canonical fields.
"""
import json
import hashlib
from pathlib import Path

DATA_FILE = Path("nsejs/data/chemistry-core2-candidates.v1.json")

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = data["questions"]
    print(f"Loaded {len(questions)} questions from {DATA_FILE}")

    # 1. Disambiguate indices 10..19 to BOND-01..10
    for idx in range(10, 20):
        num_str = f"{idx - 9:02d}"
        new_id = f"CHEM-NSEJS-BOND-{num_str}"
        questions[idx]["id"] = new_id
        questions[idx]["source_id"] = new_id
        op = questions[idx].get("op", "MODEL")
        band = questions[idx].get("band", "D2")
        score = questions[idx].get("score", 4)
        questions[idx]["source_name"] = f"NSEJS / Junior Science Chemistry · Q{num_str} · {op} · {band} (Score {score})"
        questions[idx]["raw_source_reference"] = "NSEJS / Class 9 Chemistry Foundation · Chemical Bonding"

    # 2. Enrich H2 and H3 hints for ATOM-02 through ATOM-10
    hints_enrichment = {
        "CHEM-NSEJS-ATOM-02": [
            {
                "prompt": "H1 (Isotope Formula): State the weighted average formula.",
                "text": "A_avg = sum(mass_i * abundance_i) / 100."
            },
            {
                "prompt": "H2 (Partial Contributions): Formulate the fractional mass contributions of each isotope.",
                "text": "Multiply mass of Cl-35 (34.97 u) by 0.7577 and mass of Cl-37 (36.97 u) by 0.2423."
            },
            {
                "prompt": "H3 (Crux Move): Sum the isotopic mass products and round to two decimal places.",
                "text": "Crux Move: A_avg = 26.4968 + 8.9578 = 35.4546 u; round to hundredths without truncating intermediate products."
            }
        ],
        "CHEM-NSEJS-ATOM-03": [
            {
                "prompt": "H1 (Isoelectronic Concept): Note that electron screening is nearly identical across 10 electrons.",
                "text": "For the same electron count, ionic radius is inversely related to nuclear charge Z."
            },
            {
                "prompt": "H2 (Nuclear Charge Correlation): Determine the proton count (Z) for each ion in the series.",
                "text": "Identify Z for each species: N (Z=7), O (Z=8), F (Z=9), Na (Z=11), Mg (Z=12), Al (Z=13)."
            },
            {
                "prompt": "H3 (Crux Move): Formulate the monotonic radius sequence from highest Z (tightest) to lowest Z (most expanded).",
                "text": "Crux Move: Since Z increases from 7 to 13 while electron count remains 10, the effective nuclear pull per electron is maximum for Al3+ and minimum for N3-."
            }
        ],
        "CHEM-NSEJS-ATOM-04": [
            {
                "prompt": "H1 (Energy Conservation): Equate kinetic energy to Coulomb potential energy.",
                "text": "K = (1 / 4 pi eps_0) * (q1 * q2 / r_min) = (9.0e9 * 2e * 79e) / r_min."
            },
            {
                "prompt": "H2 (Charge Product): Calculate the total charge product q1 * q2 in terms of elementary charge e.",
                "text": "Alpha particle has q1 = +2e and gold nucleus has q2 = +79e, so q1 * q2 = 158 * e^2."
            },
            {
                "prompt": "H3 (Crux Move): Rearrange the electrostatic energy equation directly for closest approach r_min.",
                "text": "Crux Move: r_min = [9.0e9 * 158 * (1.6e-19)^2] / K; substitute K = 8.0e-13 J without unit conversion errors."
            }
        ],
        "CHEM-NSEJS-ATOM-05": [
            {
                "prompt": "H1 (Kinematics of Deflection): Formulate y = (1/2) * a * t^2.",
                "text": "t = L / v, and acceleration a = e * E / m, so y = e * E * L^2 / (2 * m * v^2)."
            },
            {
                "prompt": "H2 (Transit Time and Acceleration): Express plate transit time t and transverse electrostatic acceleration a.",
                "text": "Electrons transit horizontal distance L at constant velocity v (t = L/v), experiencing vertical force F = e*E giving a = e*E/m."
            },
            {
                "prompt": "H3 (Crux Move): Invert the parabolic deflection formula to solve directly for specific charge (e/m).",
                "text": "Crux Move: e/m = (2 * y * v^2) / (E * L^2); substitute numerical values into this composite expression."
            }
        ],
        "CHEM-NSEJS-ATOM-06": [
            {
                "prompt": "H1 (Origin of Rays): Consider where the particles in each stream originate.",
                "text": "Cathode rays are electrons stripped from all matter; canal rays are residual gas cations."
            },
            {
                "prompt": "H2 (Particle Identification): Identify the constituent particles forming cathode rays vs positive canal rays.",
                "text": "Cathode rays are identical free electrons (rest mass m_e) regardless of cathode or gas material, whereas canal rays are ionized gas atoms/molecules (cations)."
            },
            {
                "prompt": "H3 (Crux Move): Relate ion mass variation to the observed charge-to-mass ratio e/m.",
                "text": "Crux Move: Since ion mass m varies directly with the atomic/molecular weight of the residual gas used in the tube, e/m of canal rays is gas-dependent, while electron e/m is a universal constant."
            }
        ],
        "CHEM-NSEJS-ATOM-07": [
            {
                "prompt": "H1 (Hund's Rule and Exchange): Count parallel spin exchange pairs.",
                "text": "For 3d5, number of possible exchange pairs is 5*4/2 = 10, whereas for 3d4 it is only 4*3/2 = 6."
            },
            {
                "prompt": "H2 (Symmetry and Exchange Energy): Correlate exchange energy with electron spin alignment.",
                "text": "Electrons with parallel spins in degenerate orbitals exchange positions, releasing stabilizing exchange energy proportional to the number of possible pairs n(n-1)/2."
            },
            {
                "prompt": "H3 (Crux Move): Compare the exchange stabilization gain against the 4s-to-3d promotion energy cost.",
                "text": "Crux Move: Transferring one electron from 4s to 3d adds 4 extra exchange pairs (10 vs 6), and the resulting exchange stabilization exceeds the small 4s-3d promotion energy."
            }
        ],
        "CHEM-NSEJS-ATOM-08": [
            {
                "prompt": "H1 (Subshell Filling): Write the subshell configuration first.",
                "text": "1s2 2s2 2p6 3s2 3p6 3d10 4s2 4p6 5s2."
            },
            {
                "prompt": "H2 (Regrouping by Principal Quantum Number): Group subshell electron counts by principal quantum number n.",
                "text": "Group orbitals by shell: K(n=1): 1s2; L(n=2): 2s2 2p6; M(n=3): 3s2 3p6 3d10; N(n=4): 4s2 4p6; O(n=5): 5s2."
            },
            {
                "prompt": "H3 (Crux Move): Verify that penultimate shell N and valence shell O obey Bohr-Bury octet bounds.",
                "text": "Crux Move: Sum the electrons in each group: K=2, L=8, M=18, N=8, O=2. Total sum equals 38, with penultimate shell N having 8 and outermost shell O having 2."
            }
        ],
        "CHEM-NSEJS-ATOM-09": [
            {
                "prompt": "H1 (Definitions): Recall definition of each term.",
                "text": "Isotopes: same Z; Isobars: same A; Isotones: same neutron count N = A - Z."
            },
            {
                "prompt": "H2 (Nucleon Arithmetic): Compute atomic number Z, mass number A, and neutron count N = A - Z for each pair.",
                "text": "For Pair 1: A=40, 40 (Z=18, 20). For Pair 2: A=14, 16; compute N=14-6 and N=16-8. For Pair 3: Z=17, 17; A=35, 37."
            },
            {
                "prompt": "H3 (Crux Move): Map each comparison strictly to its defining invariant property.",
                "text": "Crux Move: Same mass number A -> Isobars; same neutron difference N -> Isotones; same atomic number Z -> Isotopes."
            }
        ],
        "CHEM-NSEJS-ATOM-10": [
            {
                "prompt": "H1 (Hess's Law Cycle): Formulate the energy conservation loop.",
                "text": "Delta H_f = Delta H_sub + IE_1 + (1/2) Delta H_diss + Delta H_eg - U_lattice."
            },
            {
                "prompt": "H2 (Enthalpy Rearrangement): Express U_lattice in terms of formation and constituent gaseous ion energies.",
                "text": "Rearrange Hess's law cycle: U_lattice = Delta H_sub + IE_1 + (1/2)Delta H_diss + Delta H_eg - Delta H_f."
            },
            {
                "prompt": "H3 (Crux Move): Carefully track thermodynamic signs during algebraic substitution.",
                "text": "Crux Move: Substitute values keeping sign conventions: U_lattice = 108 + 496 + 122 + (-349) - (-411) kJ/mol."
            }
        ]
    }

    for qid, hints in hints_enrichment.items():
        found = False
        for q in questions:
            if q["id"] == qid:
                q["hints"] = hints
                found = True
                break
        if not found:
            print(f"WARNING: {qid} not found for hint enrichment!")

    # 3. Re-calculate exact bit-for-bit SHA-256 for all 119 stems
    mismatches_fixed = 0
    for q in questions:
        stem = q.get("stem", "")
        actual_sha = hashlib.sha256(stem.encode("utf-8")).hexdigest()
        if q.get("stem_sha256") != actual_sha:
            mismatches_fixed += 1
            q["stem_sha256"] = actual_sha

    print(f"Fixed {mismatches_fixed} SHA-256 mismatches.")

    # 4. Assert zero duplicates and all questions have >= 3 hints
    seen_ids = set()
    for q in questions:
        assert q["id"] not in seen_ids, f"Duplicate ID: {q['id']}"
        seen_ids.add(q["id"])
        hints = q.get("hints", [])
        assert len(hints) >= 3, f"{q['id']} has only {len(hints)} hints"
        actual_sha = hashlib.sha256(q["stem"].encode("utf-8")).hexdigest()
        assert q["stem_sha256"] == actual_sha, f"SHA mismatch for {q['id']}"

    print(f"All {len(questions)} questions passed sanity assertion! Writing back to {DATA_FILE}...")
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Successfully updated chemistry-core2-candidates.v1.json!")

if __name__ == "__main__":
    main()
