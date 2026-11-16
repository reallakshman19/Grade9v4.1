"""B4 hygiene: Core1A manuscripts must not disclose exact first-attempt Core1B tasks."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
CHEM=ROOT/"curriculum"/"chemistry"/"agent-b"

def test_core1a_manuscripts_do_not_publish_reserved_first_attempt_prompts():
    encountered=0
    for i in range(8,15):
        unit=f"C{i:02d}"
        text=(CHEM/"textbook"/f"{unit}.core1a.md").read_text(encoding="utf-8")
        bank=json.loads((CHEM/"core1b"/f"{unit}.core1b.v0.1.0.json").read_text(encoding="utf-8"))
        for task in bank["cycles"]:
            assert task["attempt"]["prompt"] not in text, task["cycle_id"]
            assert task["attempt"]["initial_answer_visibility"]=="HIDDEN"
            assert task["attempt"]["first_attempt_must_be_saved_before_feedback"]
            encountered+=1
    assert encountered==120
