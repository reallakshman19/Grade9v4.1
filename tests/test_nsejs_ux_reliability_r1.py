"""NSEJS UX Reliability R1: seven low-change, fail-closed improvements.
These are engineering assertions, not source-authenticity or academic approval.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SUBJECTS={"physics":(109,6),"chemistry":(119,6),"biology":(119,5)}


def read(path):
    return (ROOT/path).read_text(encoding="utf-8")


def test_all_subjects_have_visible_verification_failure_and_loading_states():
    for subject in SUBJECTS:
        page=read(f"nsejs/{subject}/index.html")
        code=read(f"nsejs/js/core2-{subject}-reader.js")
        assert page.count('id="qbLoadNotice"')==1
        assert 'role="status" aria-live="polite"' in page
        assert 'id="qbResultCount" aria-live="polite">Checking verified candidate records…' in page
        assert 'setBankNotice("Verifying' in code
        assert 'setBankNotice("");' in code
        assert 'setBankNotice(' in code and 'true);' in code
        assert 'role", failed ? "alert" : "status"' in code
        assert 'retry.addEventListener("click", () => location.reload())' in code
        assert "No answer" in code or "No unverified questions" in code
        assert "answerBox.hidden = true" in code


def test_question_search_excludes_postcommit_only_keys_steps_and_crux():
    for subject in SUBJECTS:
        code=read(f"nsejs/js/core2-{subject}-reader.js")
        start=code.index("function applyFilters(")
        end=code.index("// 5. Sorting",start)
        filtering=code[start:end]
        for forbidden in ("const ansLower","const stepsLower","const cruxLower",
                          "q.answer","q.steps","q.crux_move_ref"):
            assert forbidden not in filtering,(subject,forbidden)
        assert "const full =" in filtering and "optsLower" in filtering
        assert "idLower" in filtering and "srcLower" in filtering
        # Keys and worked solutions remain behind the existing post-attempt UI.
        assert "q.answer" in code and "q.steps" in code


def test_return_to_all_topics_clears_question_search_and_moves_focus():
    for subject in SUBJECTS:
        code=read(f"nsejs/js/core2-{subject}-reader.js")
        page=read(f"nsejs/{subject}/index.html")
        assert 'onclick="window.returnToAllTopics()"' in page
        assert "Return to all topics · clear filters" in page
        start=code.index("window.returnToAllTopics = function()")
        chunk=code[start:start+450]
        assert "window.resetFilters()" in chunk
        assert 'document.getElementById("topicsGrid")' in chunk
        assert "scrollIntoView" in chunk and "focus(" in chunk


def test_dynamic_counts_not_asserted_before_data_is_verified():
    for subject,(total,topics) in SUBJECTS.items():
        page=read(f"nsejs/{subject}/index.html")
        code=read(f"nsejs/js/core2-{subject}-reader.js")
        assert "Checking verified candidate records…" in page
        assert 'id="qbResultCount" aria-live="polite">Showing ' not in page
        assert "candidate questions across " in code
        assert "applyFilters(Boolean(initialHash || initialQ))" in code
        assert str(total) in page  # candidate route description, not verified load
        assert 'id="qbFilters"' in page and 'id="topicWorkspace"' in page


def test_resume_is_same_site_lesson_only_and_does_not_touch_attempts():
    nav=read("site-nav.js")
    assert "function resumeLesson(relative,base)" in nav
    assert "resumeLesson(relative,base);" in nav
    assert '"g9v41:last-lesson:"+subject' in nav
    assert "url.origin!==location.origin" in nav
    assert "url.pathname.startsWith(prefix)" in nav
    assert "curriculum" in nav and "core1" in nav
    assert 'new URL(stored,location.origin).href' in nav
    assert 'a.dataset.g9Resume=subject' in nav
    assert '"ph","unit","subtopic","mode"' in nav
    assert "localStorage.setItem(key,safe.pathname+safe.search)" in nav
    resume=nav.split("function resumeLesson(relative,base)")[1].split("function mount()")[0]
    assert "firstAttempt" not in resume and "saveAttempt" not in resume
    for subject in SUBJECTS:
        page=read(f"nsejs/{subject}/index.html")
        selector={"physics":"g9-primary-study-routes",
                  "chemistry":"chem-primary-routes",
                  "biology":"biology-primary-routes"}[subject]
        assert f'nav class="{selector}"' in page


def test_header_changes_trigger_physics_browser_navigation():
    workflow=read(".github/workflows/nsejs-physics-learner-navigation-r1.yml")
    assert '- "site-nav.js"' in workflow
    assert "node --check site-nav.js" in workflow
    assert "python tools/physics_navigation_browser_qa.py" in workflow


def test_real_chromium_regressions_cover_three_banks_and_negative_controls():
    code=read("tools/nsejs_bank_ux_regression_r1.py")
    for subject in SUBJECTS:
        assert f'"{subject}":' in code
    for phrase in ("failure_is_visible","resume_only_safe_lesson_urls",
                   "hidden_term","Return to all topics","qbLoadNotice",
                   "count()==0","role","g9-protected-attempt:fixture"):
        assert phrase in code
