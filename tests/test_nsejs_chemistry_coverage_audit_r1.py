"""Data-integrity tests for the R00 Chemistry coverage audit package.
These tests do NOT independently qualify Chemistry, QRT difficulty, or past exam sources.
"""
from __future__ import annotations
import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs" / "audits" / "chemistry-c01-c14"

def read_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

class ChemistryCoverageAuditR1(unittest.TestCase):
    def setUp(self):
        self.matrix = read_json("CHEMISTRY_C01_C14_EVIDENCE_MATRIX_R1.json")
        self.gaps = read_json("CHEMISTRY_MISSING_CONTENT_AND_GATES_R1.json")

    def test_unique_84_ids_and_unit_total(self):
        rows = self.matrix["rows"]
        self.assertEqual(len(rows), 84)
        ids = [r["subtopic_id"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(self.matrix["unit_summary"]), 14)
        self.assertEqual(sum(x["subtopics"] for x in self.matrix["unit_summary"].values()), 84)
        self.assertEqual(sum(r["core1b_authored_cycles"] for r in rows), 252)

    def test_per_item_qrts_are_three_distinct_and_unqualified(self):
        for row in self.matrix["rows"]:
            self.assertEqual(row["cognitive_operation_count"], 3, row["subtopic_id"])
            self.assertEqual(len(set(row["qrt_template_refs"])), 3, row["subtopic_id"])
            self.assertEqual(row["qrt_author_binding"], "PASS")
            self.assertEqual(row["core1b_six_stage_record"], "PASS")
            self.assertEqual(row["official_source_review"], "HOLD")
            self.assertEqual(row["independent_scientific_review"], "HOLD")
            self.assertEqual(row["independent_qrt_review"], "HOLD")

    def test_explicit_source_failures_cannot_be_silently_approved(self):
        rows = self.matrix["rows"]
        failed = {r["subtopic_id"] for r in rows if r["qualification_disposition"] == "FAIL"}
        self.assertEqual(failed, {"CHEM-C11.05", "CHEM-C14.01"})
        self.assertEqual(sum(r["qualification_disposition"] == "HOLD" for r in rows), 82)
        self.assertEqual(sum(r["qualification_disposition"] == "PASS" for r in rows), 0)
        self.assertEqual(self.matrix["counts"]["inventory_PASS"], 84)
        self.assertEqual(self.matrix["counts"]["overall_PASS"], 0)

    def test_csv_json_exact_row_reconciliation(self):
        with (ROOT / "CHEMISTRY_C01_C14_EVIDENCE_MATRIX_R1.csv").open(
            encoding="utf-8", newline=""
        ) as f:
            records = list(csv.DictReader(f))
        self.assertEqual(len(records), 84)
        ref = {r["subtopic_id"]: r for r in self.matrix["rows"]}
        for row in records:
            self.assertIn(row["subtopic_id"], ref)
            self.assertEqual(row["scope"], ref[row["subtopic_id"]]["scope"])
            self.assertEqual(row["qualification_disposition"], ref[row["subtopic_id"]]["qualification_disposition"])

    def test_gap_register_and_source_shas_are_custodial(self):
        self.assertEqual(len(self.gaps["issues"]), 14)
        self.assertEqual(sum(x["status"] == "FAIL" for x in self.gaps["issues"]), 2)
        self.assertEqual(sum(x["status"] == "HOLD" for x in self.gaps["issues"]), 12)
        pins = self.matrix["source_heads"]
        self.assertEqual(pins["agent_A_PR6"], "fb5cf6626088a1312743d60d0c39d06a4a3f8133")
        self.assertEqual(pins["P00_PR17_B_combined"], "df3b77723e59974bab107ee8e11d12b625418579")
        self.assertEqual(self.matrix["unique_template_count"], 10)
        self.assertEqual(self.matrix["counts"]["physical_staged_cycles"], 39)

if __name__ == "__main__":
    unittest.main()
