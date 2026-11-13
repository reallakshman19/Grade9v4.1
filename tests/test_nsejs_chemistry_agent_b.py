"""Agent B C08–C14 draft integration guards; technical only, never academic admission."""
from __future__ import annotations
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHEM = ROOT / "curriculum" / "chemistry"
B = CHEM / "agent-b"
UNITS = tuple(f"C{i:02d}" for i in range(8, 15))
OPS = {"RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"}
HOLD = {"ACADEMIC_HOLD", "CANDIDATE", "DRAFT"}

def read(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)

class TestAgentBCandidate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.syllabus = read(CHEM / "syllabus" / "chemistry-syllabus.v1.json")
        cls.source_units = {u["id"]: u for u in cls.syllabus["units"]}
        cls.adapters = {u: read(CHEM / "adapters" / f"{u}.v1.json") for u in UNITS}
        cls.records = {u: read(B / "canonical" / f"{u}.concepts.v0.1.0.json") for u in UNITS}

    def test_exact_agent_b_syllabus_ids_40(self):
        self.assertEqual(sum(len(self.source_units[u]["subtopics"]) for u in UNITS), 40)
        for unit in UNITS:
            ids = {x["id"] for x in self.source_units[unit]["subtopics"]}
            adapter_ids = {x["subtopic_id"] for x in self.adapters[unit]["subtopics"]}
            canon_ids = {x["subtopic_id"] for x in self.records[unit]["concepts"]}
            self.assertEqual(ids, adapter_ids, unit)
            self.assertEqual(ids, canon_ids, unit)

    def test_contract_and_exact_qrt_templates(self):
        count = 0
        for unit, adapter in self.adapters.items():
            self.assertEqual(adapter["schema"], "g9v41-chem-topic-adapter/v1")
            self.assertEqual(adapter["subject"], "CHEMISTRY")
            self.assertEqual(adapter["unit_id"], unit)
            self.assertEqual(adapter["blueprint_ref"], "CHEM-QRT-BLUEPRINT@0.1.0")
            self.assertEqual(adapter["syllabus_ref"], "chemistry-syllabus.v1.json@0.1.0")
            self.assertEqual(adapter["status"], "ACADEMIC_HOLD")
            concepts = {x["concept_id"] for x in self.records[unit]["concepts"]}
            for sub in adapter["subtopics"]:
                operations = []
                for task in sub["qrt_instances"]:
                    count += 1
                    operations.append(task["primary_operation"])
                    self.assertIn(task["primary_operation"], OPS)
                    self.assertEqual(task["template_ref"], f'QRT-{task["primary_operation"]}-{task["band"]}')
                    self.assertIn(task["band"], ("D3", "D4"))
                    self.assertIn(task["canonical_concept_refs"][0], concepts)
                    self.assertEqual(set(task["slots"]), {"X", "Y", "Z", "W"})
                    self.assertTrue(all(task["slots"][k].strip() for k in ("X", "Y", "Z", "W")))
                    self.assertEqual(task["status"], "ACADEMIC_HOLD")
                self.assertGreaterEqual(len(set(operations)), 3, sub["subtopic_id"])
        self.assertEqual(count, 120)

    def test_scope_and_prerequisite_nonpromotion(self):
        for unit in UNITS:
            source = {s["id"]: s for s in self.source_units[unit]["subtopics"]}
            for item in self.adapters[unit]["subtopics"]:
                self.assertEqual(item["scope"], source[item["subtopic_id"]]["scope"])
                self.assertTrue(item["missing_prerequisite_refs"])
                self.assertNotEqual(item["canonical_truth_status"], "QUALIFIED")
            for concept in self.records[unit]["concepts"]:
                self.assertEqual(concept["academic_status"], "DRAFT_UNREVIEWED")
                self.assertEqual(concept["exam_provenance_claim"], "NONE")

    def test_c09_textbook_is_unit_scope_not_oxyacid_key(self):
        text = (B / "textbook" / "C09.core1a.md").read_text(encoding="utf-8")
        for i in range(1, 7):
            self.assertIn(f"C09.{i:02d}", text)
        self.assertGreater(len(text.split()), 2000)
        self.assertIn("EXTENSION", text)
        self.assertIn("neutralisation", text.lower())
        self.assertIn("washing soda", text.lower())
        self.assertIn("independent check", text.lower())

    def test_c09_core1b_attempt_first_closed_and_joined(self):
        data = read(B / "core1b" / "C09.core1b.v0.1.0.json")
        cycles = data["cycles"]
        self.assertEqual(len(cycles), 18)
        adapter_refs = {t["instance_id"] for s in self.adapters["C09"]["subtopics"] for t in s["qrt_instances"]}
        self.assertEqual(adapter_refs, {c["qrt_instance_ref"] for c in cycles})
        review_keys = {f"{g}{n}" for g in "HSPM" for n in range(1, 4)}
        for c in cycles:
            self.assertEqual(c["source_role"], "AUTHORED_PRACTICE")
            self.assertIsNone(c["source_exam_question_id"])
            self.assertTrue(c["attempt"]["first_attempt_must_be_saved_before_feedback"])
            self.assertEqual(c["attempt"]["initial_answer_visibility"], "HIDDEN")
            self.assertTrue(c["attempt"]["post_commit_closure"]["model_response"])
            self.assertEqual([h["id"] for h in c["attempt"]["hints"]], ["H1", "H2", "H3"])
            self.assertEqual(set(c["reviews"]), review_keys)
            self.assertTrue(all(v == "UNREVIEWED" for v in c["reviews"].values()))
            for step in ("predict", "attempt", "reconstruct", "diagnose", "repair", "boundary_test"):
                self.assertIn(step, c)
            self.assertTrue(c["boundary_test"]["answer"])
        self.assertEqual(data["release"]["academic_release"] if "academic_release" in data["release"] else data["release"]["scientific_review"], "HOLD")

    def test_c09_capstone_author_vectors_not_qualification(self):
        data = read(B / "qrt" / "C09-D3D4-capstone-evidence.v0.1.0.json")
        self.assertEqual(len(data["tasks"]), 12)
        expected = {"D3": (6, 7), "D4": (8, 10)}
        ids = set()
        for t in data["tasks"]:
            self.assertNotIn(t["task_id"], ids)
            ids.add(t["task_id"])
            self.assertIsNone(t["source_question_ref"])
            self.assertEqual(t["academic_review"], "HOLD")
            score = t["self_score_proposal"]
            self.assertEqual(score["status"], "AUTHOR_PROPOSAL_NOT_INDEPENDENT")
            self.assertEqual(sum(score["scores"].values()), score["total"])
            lo, hi = expected[t["band_candidate"]]
            self.assertTrue(lo <= score["total"] <= hi)
            self.assertEqual(t["template_ref"], f'QRT-{t["primary_operation"]}-{t["band_candidate"]}')
        self.assertEqual(len({t["subtopic_id"] for t in data["tasks"]}), 6)

if __name__ == "__main__":
    unittest.main()
