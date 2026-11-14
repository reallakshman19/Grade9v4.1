"""Chemistry Stage 0/1 technical contract smoke tests.

These tests check shapes and joins only, not scientific truth or academic admission.
"""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHEM = ROOT / "curriculum" / "chemistry"
OPS = ("RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY")
BANDS = {"D1": (0, 2), "D2": (3, 5), "D3": (6, 7), "D4": (8, 10)}

def get(relative):
    return json.loads((CHEM / relative).read_text(encoding="utf-8"))

class ChemistryStage01Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.syl = get("syllabus/chemistry-syllabus.v1.json")
        cls.core = get("contracts/chem-core-authority.v0.1.0.json")
        cls.bp = get("blueprint/chemistry-qrt.D3-D4.v0.1.0.json")
        cls.schema = get("contracts/chem-topic-adapter.schema.v0.1.0.json")
        cls.index = get("registry/topic-adapter-index.v0.1.0.json")
        cls.sample = get("examples/C07-ionic-bonding-adapter.v0.1.0.json")

    def test_baseline_and_distinct_ownership(self):
        self.assertEqual(self.syl["unit_count"], 14)
        units = self.syl["units"]
        self.assertEqual([u["id"] for u in units], [f"C{i:02}" for i in range(1, 15)])
        self.assertEqual([u["owner_agent"] for u in units], ["A"] * 7 + ["B"] * 7)
        self.assertEqual(len(self.index["units"]), 14)
        self.assertEqual({u["unit_id"] for u in self.index["units"]}, {u["id"] for u in units})

    def test_subtopic_unique_ids_three_distinct_planned_operations(self):
        all_ids = []
        for u in self.syl["units"]:
            for sub in u["subtopics"]:
                self.assertTrue(sub["id"].startswith("CHEM-" + u["id"] + "."))
                ops = sub["planned_qrt_operations"]
                self.assertGreaterEqual(len(set(ops)), 3)
                self.assertTrue(set(ops).issubset(OPS))
                self.assertEqual(sub["academic_status"], "HOLD")
                all_ids.append(sub["id"])
        self.assertEqual(len(all_ids), len(set(all_ids)))
        self.assertEqual(len(all_ids), self.syl["subtopic_count"])
        self.assertEqual(self.syl["planned_demand_count"], 3 * len(all_ids))

    def test_blueprint_14_cells_and_evidence_asks(self):
        self.assertEqual(self.bp["operation_order"], list(OPS))
        self.assertEqual(len(self.bp["cells"]), 14)
        for band in ("D3", "D4"):
            for i, op in enumerate(OPS, 1):
                cell = self.bp["cells"][f"{band}.{i}"]
                self.assertEqual(cell["template_ref"], f"QRT-{op}-{band}")
                self.assertEqual(cell["operation"], op)
                self.assertEqual(len(cell["reviewer_questions"]), 12)
                self.assertTrue(cell["protected_work"])
                self.assertTrue(cell["chemistry_warrant"])
        self.assertEqual(self.bp["status"], "DRAFT_OWNER_ACADEMIC_REVIEW")

    def test_authority_and_source_pins(self):
        pins = {p["authority"]: p for p in self.core["source_pins"]}
        self.assertEqual(pins["28_QRT_TEMPLATES"]["template_count"], 28)
        self.assertEqual(pins["28_QRT_TEMPLATES"]["git_blob_sha"], self.bp["pins"]["template_library"]["git_blob_sha"])
        self.assertEqual(self.core["qrt_contract"]["score_range_per_band"], {k: list(v) for k, v in BANDS.items()})
        self.assertEqual(self.syl["baseline_commit"], self.index["baseline_commit"])
        self.assertEqual(self.core["baseline_commit"], self.syl["baseline_commit"])

    def test_sample_adapter_joins_and_protected_moves(self):
        sub = self.sample["subtopics"][0]
        self.assertEqual(self.sample["unit_id"], "C07")
        syllabus_sub = {s["id"] for u in self.syl["units"] for s in u["subtopics"]}
        self.assertIn(sub["subtopic_id"], syllabus_sub)
        self.assertGreaterEqual(len(sub["qrt_instances"]), 3)
        self.assertEqual(len({q["primary_operation"] for q in sub["qrt_instances"]}), 3)
        known_refs = {c["template_ref"] for c in self.bp["cells"].values()}
        for item in sub["qrt_instances"]:
            self.assertIn(item["template_ref"], known_refs)
            self.assertEqual(item["template_ref"], f"QRT-{item['primary_operation']}-{item['band']}")
            self.assertEqual(set(item["slots"]), {"X", "Y", "Z", "W"})
            self.assertTrue(all(item["slots"].values()))
            self.assertTrue(item["student_task"] and item["wrong_idea"] and item["independent_check"])
        self.assertNotEqual(sub["canonical_truth_status"], "QUALIFIED")
        self.assertEqual(self.sample["status"], "CANDIDATE")

    def test_fail_closed_and_no_fabricated_publication(self):
        self.assertEqual(self.syl["baseline_evidence"]["candidate_review_status"], "NOT_ADMITTED")
        self.assertEqual(self.core["release_status"]["qrt_academic"], "HOLD")
        self.assertEqual(self.core["release_status"]["production"], "NOT_AUTHORIZED")
        for unit in self.index["units"]:
            if unit["owner_agent"] == "A":
                self.assertIn(
                    unit["adapter_status"],
                    {"NOT_AUTHORED", "AUTHOR_COMPLETE_ACADEMIC_HOLD"},
                )
            else:
                self.assertEqual(unit["adapter_status"], "NOT_AUTHORED")
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")

if __name__ == "__main__":
    unittest.main()
