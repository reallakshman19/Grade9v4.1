"""Native Chemistry author reader — source-specific missing topic fixes, technical only.

The original 39 B02 task IDs are unchanged; this suite only checks the three
source-specific Core1A explanations and their protected Stage 6 transfers.
"""
import pytest
import re
from test_nsejs_chemistry_agent_b_browser import browser,server,open_page

@pytest.mark.parametrize("viewport",[(1600,1000),(1000,1600)])
@pytest.mark.parametrize("unit,subindex,task_id,teaching_terms,answer_term",[
 ("C11",4,"CORE1B-C11-05-1-B02-R2",
  ["haloalkane","1-chloropropane","2-chloropropane"],"1-chloropropane"),
 ("C14",0,"CORE1B-C14-01-2",
  ["chlorofluorocarbons","stratospheric ozone","Cl·"],"not instantaneous"),
 ("C14",4,"CORE1B-C14-05-1",
  ["non-biodegradable","polyethylene","microorganisms"],"Conventional PE")
])
def test_source_gap_teaching_and_protected_changed_condition(
        browser,unit,subindex,task_id,teaching_terms,answer_term,viewport):
    ctx,page=open_page(browser,unit,*viewport)
    try:
        page.locator("#sections button").nth(subindex).click()
        lesson=page.locator("article").inner_text()
        for term in teaching_terms:
            assert term.lower() in lesson.lower(),f"{unit}: missing source teaching {term}"
        page.get_by_role("button",name="Core1B independent practice").click()
        page.get_by_role("heading",name="Stage 1 — Predict").wait_for()
        page.locator("#task-select").select_option(task_id)
        page.get_by_role("heading",name="Stage 2 — Independent attempt").wait_for()
        # The merged P00 runtime labels protected feedback differently from
        # Agent B's earlier preview; both must remain concealed before commit.
        model_heading=page.get_by_role(
            "heading",name=re.compile(
                r"^Model response(?: · POST-COMMIT| \(post-commit\))$",re.I
            )
        )
        assert model_heading.count()==0
        assert page.locator("#boundary-answer").count()==0
        page.locator("#prediction-answer").fill(
            "I predict a model change based on chemical identity and evidence.")
        page.locator("#original-answer").fill(
            "I compare at least two chemical explanations and check system boundaries.")
        page.locator("#commit-attempt").click()
        model_heading.wait_for(timeout=15000)
        prompt=page.locator("article").inner_text()
        assert "Stage 6 — Changed-condition boundary test" in prompt
        assert page.locator("#boundary-answer").count()==1
        assert not re.search(r"Model response(?: \(post boundary answer\))?:",prompt)
        page.locator("#boundary-answer").fill(
            "I apply the chemical model to the new boundary and identify what would change.")
        page.locator("#reveal-boundary").click()
        page.get_by_text(
            re.compile(r"Model response(?: \(post boundary answer\))?:")
        ).wait_for(timeout=15000)
        assert answer_term.lower() in page.locator("article").inner_text().lower()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 3")
    finally:
        ctx.close()
